from typing import Union

from pydantic import BaseModel


class VideoBase(BaseModel):
    title: str
    author: str
    description: Union[str, None] = None
    # avatar: str
    # video_url: str
    # is_follow: bool
    # like_num: int
    # collect_num: int
    # comment_nu: int
    # share_num: int


class VideoCreate(VideoBase):
    pass


class Video(VideoBase):
    id: int
    owner_id: int
    create_time: str

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
    videos: list[Video] = []

    class Config:
        orm_mode = True
