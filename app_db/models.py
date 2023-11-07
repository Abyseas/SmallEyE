from datetime import datetime

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship

from .database import Base
from app_utils.custom_schemas import VideoCategoryType


def calc_sort_score(context):
    print(type(context))


class User(Base):
    """
    用户表
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=False)
    avatar_key = Column(String, default='avatar/0-default_header.png')
    follow_cnt = Column(Integer, default=0)
    like_cnt = Column(Integer, default=0)
    fans_cnt = Column(Integer, default=0)

    videos = relationship("Video", back_populates="owner")


class Video(Base):
    """
    短视频表
    """
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    author = Column(String, index=True, nullable=False)
    create_time = Column(DateTime, default=datetime.now)
    video_key = Column(String, nullable=False)
    avatar_key = Column(String, nullable=False)
    cover_key = Column(String, nullable=False)
    category = Column(Enum(VideoCategoryType), default="no classify")
    like_cnt = Column(Integer, default=0)
    collect_cnt = Column(Integer, default=0)
    comment_cnt = Column(Integer, default=0)
    share_cnt = Column(Integer, default=0)
    # sort_score = Column(Integer, default=calc_sort_score)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="videos")
