# built-in
from typing import Union
import time
import json
import requests

# fastAPI relate
import uvicorn
from fastapi import FastAPI, APIRouter
from fastapi import Form, File, UploadFile, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import qiniu

# self define
from app_utils.aux_tools import q, bucket, before_upload_data, base_domain
from app_utils.use_type import VideoCategoryType
from app_db.database import engine, get_db
from app_db import schemas, crud, models
from app_login import login_router

# FastAPI application
app = FastAPI()
router_database = APIRouter(prefix="/database", tags=["database"])

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
models.Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return "Hello FastAPI"


@app.get("/list/{bucket_name}")
def read_bucket_video_list(bucket_name: str, prefix: Union[str] = None, marker: Union[str] = None,
                           limit: Union[int] = None, delimiter: Union[str] = None):
    eof = False
    ret = info = None
    video_list = []
    video_id = 1
    while not eof:
        ret, eof, info = bucket.list(bucket_name, f"{prefix}/video/", marker, limit, delimiter)
        if ret and not ret.get('marker'):
            eof = True
        marker = ret.get("marker")
        video_items = ret.get("items")
        for v in video_items:
            if v.get("mimeType") != "application/qiniu-object-manager":
                meta_key = f"{prefix}/manifest/video/{v.get('key').split('/')[-1]}.json"
                meta_url = q.private_download_url(f"{base_domain}/{meta_key}")
                metadata = requests.get(meta_url).json()
                print("json@@@", metadata, meta_url)
                put_time = time.strftime("%Y/%m/%d %H:%M:%S",
                                         time.localtime(v.get('putTime') // (10 ** 7)))
                video_list.append({
                    "id": video_id,
                    "avatar": None,
                    "username": metadata.get("username"),
                    "user_id": metadata.get("user_id"),
                    "is_follow": metadata.get("is_follow"),
                    "title": metadata.get("title"),
                    "cover": None,
                    "video_url": q.private_download_url(f"{base_domain}/{v.get('key')}"),
                    "create_time": put_time,
                    "like_num": metadata.get("like_num"),
                    "collect_num": metadata.get("collect_num"),
                    "comment_num": metadata.get("comment_num"),
                    "share_num": metadata.get("share_num")
                })
                video_id += 1

    return {
        "code": info.status_code,
        "msg": info.json().get("error", "success"),
        "data": {
            "total": len(video_list),
            "list": video_list
        }
    }


@app.post("/upload/{bucket_name}")
async def upload_source(bucket_name: str, file: UploadFile = File(), metadata: str = Form()):
    """upload source

    """
    file_bytes = await file.read()
    title = file.filename
    # with open(f"./data/upload/{title}", 'wb') as f:
    #     f.write(file_bytes)
    data = json.loads(metadata)
    user_id = data.get('user_id')
    media_type = data.get("media_type")

    key = f"user@{user_id}/{media_type}/{title}"
    token = q.upload_token(bucket_name)
    before_upload_data(key)
    ret, info = qiniu.put_data(token, key, file_bytes)
    meta_key = f"user@{user_id}/manifest/{media_type}/{title}.json"
    before_upload_data(meta_key)
    qiniu.put_data(token, meta_key, metadata)

    return ret


# DataBase operation
@router_database.get("/users", response_model=list[schemas.User])
def read_users(db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router_database.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router_database.post("/users/create", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="UserName already registered")
    return crud.create_user(db=db, user=user)


@router_database.get("/videos", response_model=list[schemas.Video])
def read_videos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    videos = crud.get_videos(db, skip=skip, limit=limit)
    return videos


@router_database.get("/videos/category/{category}", response_model=list[schemas.Video])
def read_category_videos(category: VideoCategoryType, db: Session = Depends(get_db)):
    videos = crud.get_videos_by_category(db, category)
    return videos


@router_database.get("/videos/user/{username}", response_model=list[schemas.Video])
def read_user_videos(username: str, db: Session = Depends(get_db)):
    videos = crud.get_videos_by_username(db, username)
    return videos


@router_database.post("/videos/{user_id}/create", response_model=schemas.Video)
def create_video_for_user(user_id: int, video: schemas.VideoCreate,
                          db: Session = Depends(get_db)):
    return crud.create_user_video(db=db, video=video, user_id=user_id)


# include sub router
app.include_router(router_database)
app.include_router(login_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
