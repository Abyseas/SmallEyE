from typing import Union
from datetime import datetime, timedelta

import qiniu
from fastapi import Depends, APIRouter, HTTPException, status, Request
from fastapi import File, Form, UploadFile
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt

from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app_utils.CONST import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, pipline_name
from app_utils.exception import ResException, ExceptionCode
from app_utils.aux_tools import q, bucket_name, before_upload_data
from app_utils.custom_schemas import VideoCategoryType
from app_db import schemas, crud, models
from app_db.database import get_db
from .login_model import Token, TokenData

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login/token", auto_error=False)
login_router = APIRouter(prefix='/login', tags=["login"])


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(username: str, password: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, username=username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    if not token:
        raise ResException(
            code=ExceptionCode.NO_AUTHENTICATE,
            error="Not authenticated, please make sure you have this header(Authorization: Bearer Your_Access_Token)",
            headers={"WWW-Authenticate": "Bearer"},
        )
    credentials_exception = ResException(
        code=ExceptionCode.CREDENTIALS_NOT_VALIDATE,
        error="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        # sub 属性会被校验，必须是str属性
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=int(user_id))
    except JWTError as e:
        raise credentials_exception
    user = crud.get_user(db, user_id=token_data.user_id)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: schemas.User = Depends(get_current_user)):
    if not current_user.is_active:
        raise ResException(
            code=ExceptionCode.USER_NOT_ACTIVE,
            error="Inactive user"
        )
    return current_user


@login_router.post("/token", response_model=schemas.BaseResponse)
async def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user: models.User = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise ResException(
            code=ExceptionCode.INCORRECT_USER_OR_PASSWORD,
            error="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    if not user.is_active:
        raise ResException(
            code=ExceptionCode.USER_NOT_ACTIVE,
            error="Inactive user"
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    # return {
    #             "access_token": access_token,
    #             "token_type": "bearer"
    #         }
    return {
        "code": status.HTTP_200_OK,
        "message": "Access token create",
        "data": {
            "access_token": access_token,
            "token_type": "bearer"
        }
    }


@login_router.get("/validate/{register_token}", response_model=schemas.BaseResponse)
async def validate_register_token(register_token: str, db: Session = Depends(get_db)):
    credentials_exception = ResException(
        code=ExceptionCode.CREDENTIALS_NOT_VALIDATE,
        error="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(register_token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("username")
        password = payload.get("password")
        if username is None:
            raise credentials_exception
    except JWTError as e:
        raise credentials_exception
    user: models.User = authenticate_user(username, password, db)
    if not user:
        raise ResException(
            code=ExceptionCode.INCORRECT_USER_OR_PASSWORD,
            error="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    cnt = crud.update_user_by_username(db, username, "is_active", True)
    return {
        "code": status.HTTP_200_OK,
        "message": "User is activated, please login now",
        "data": {
            "update_count": cnt,
            "register_token": register_token
        }
    }


@login_router.get("/users/me", response_model=schemas.UserResponse)
async def read_users_me(current_user: schemas.User = Depends(get_current_active_user)):
    return {
        "code": status.HTTP_200_OK,
        "message": "Your info get successfully",
        "data": current_user
    }


@login_router.get("/users/me/videos", response_model=schemas.VideoResponse)
async def read_my_videos(current_user: schemas.User = Depends(get_current_active_user)):
    return {
        "code": status.HTTP_200_OK,
        "message": "Your video info get successfully",
        "data": current_user.videos
    }


@login_router.post("/videos/me/upload", response_model=schemas.VideoResponse)
async def upload_my_video(title: str = Form(), category: VideoCategoryType = Form(), file: UploadFile = File(),
                          current_user: schemas.User = Depends(get_current_active_user),
                          db: Session = Depends(get_db)):
    video = schemas.VideoCreate(title=title, author=current_user.username, category=category)
    file_bytes = await file.read()
    token = q.upload_token(bucket_name)
    user_id = current_user.id
    key = f"{user_id}-{title}"
    suffix = file.filename.split('.')[-1]
    video.video_key = f"video/{key}.{suffix}"
    video.avatar_key = current_user.avatar_key
    video.cover_key = f"cover/{key}.png"

    # video upload
    before_upload_data(video.video_key)
    ret, info = qiniu.put_data(token, video.video_key, file_bytes)

    # cover auto generate
    fops = "vframe/png/offset/1"
    saveas_key = qiniu.urlsafe_base64_encode(f"{bucket_name}:{video.cover_key}")
    fops = fops + "|saveas/" + saveas_key
    pfop = qiniu.PersistentFop(q, bucket_name, pipline_name)
    ops = [fops]
    ret, info = pfop.execute(video.video_key, ops, 1)

    video = crud.create_user_video(db=db, video=video, user_id=user_id)
    return {
        "code": status.HTTP_200_OK,
        "message": f"You have successfully create a video",
        "data": video
    }
