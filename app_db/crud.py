# create, read, update, delete
from typing import Union

from sqlalchemy.orm import Session

from . import models, schemas
from app_login import get_password_hash
from app_utils.aux_tools import q, base_domain, get_outbound_link
from app_utils.custom_schemas import VideoCategoryType


def video_process(video: models.Video):
    video.video_url = get_outbound_link(video.video_key)
    video.avatar_url = get_outbound_link(video.avatar_key)
    video.cover_url = get_outbound_link(video.cover_key)


def videos_process(videos: list[models.Video] = None):
    if videos:
        for video in videos:
            video_process(video)


def user_videos_process(user: models.User = None):
    if user:
        videos_process(user.videos)


def get_user(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    user_videos_process(user)
    return user


def get_user_by_username(db: Session, username: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    user_videos_process(user)
    return user


def get_user_by_email(db: Session, email: str):
    user = db.query(models.User).filter(models.User.email == email).first()
    user_videos_process(user)
    return user


def get_users(db: Session, skip: int = 0, limit: int = 10):
    users = db.query(models.User).offset(skip).limit(limit).all()
    for user in users:
        user_videos_process(user)
    return users


def update_user_by_username(db: Session, username: str, key: str, value: Union[str, int]):
    cnt = db.query(models.User).filter(models.User.username == username).update({key: value})
    db.commit()
    return cnt


def delete_user(db: Session, user_id: int):
    del_data = db.query(models.User).filter(models.User.id == user_id).delete()
    db.commit()
    return del_data


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_videos(db: Session, skip: int = 0, limit: int = 10):
    videos = db.query(models.Video).offset(skip).limit(limit).all()
    videos_process(videos)
    return videos


def get_videos_by_category(db: Session, category: VideoCategoryType, skip: int = 0,
                           limit: int = 10):
    videos = db.query(models.Video).filter(models.Video.category == category)\
        .offset(skip).limit(limit).all()
    videos_process(videos)
    return videos


def get_videos_by_username(db: Session, username: str, skip: int = 0, limit: int = 0):
    videos = db.query(models.Video).filter(models.Video.author == username)\
        .offset(skip).limit(limit).all()
    videos_process(videos)
    return videos


def create_user_video(db: Session, video: schemas.VideoCreate, user_id: int):
    db_video = models.Video(**video.model_dump(), owner_id=user_id)
    db.add(db_video)
    db.commit()
    db.refresh(db_video)
    video_process(db_video)
    return db_video
