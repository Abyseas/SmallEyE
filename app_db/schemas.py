from typing import Union
from datetime import datetime

from pydantic import BaseModel

from app_utils.custom_schemas import VideoCategoryType


class VideoBase(BaseModel):
    title: str
    author: str
    category: VideoCategoryType


class VideoCreate(VideoBase):
    video_key: str
    avatar_key: str
    cover_key: str


class Video(VideoBase):
    id: int
    owner_id: int
    create_time: datetime
    video_url: str
    avatar_url: str
    cover_url: str
    like_count: int
    collect_count: int
    comment_count: int
    share_count: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool = False
    follow_sum: int
    like_sum: int
    fans_sum: int
    videos: list[Video] = []

    class Config:
        orm_mode = True


class BaseResponse(BaseModel):
    code: int
    message: str
    data: dict = None


class UserResponse(BaseResponse):
    data: Union[User, list[User]]


class VideoResponse(BaseResponse):
    data: Union[Video, list[Video]]