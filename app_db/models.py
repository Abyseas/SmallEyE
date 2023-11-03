from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    """
    用户表
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    videos = relationship("Video", back_populates="owner")


class Video(Base):
    """
    短视频表
    """
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    author = Column(String, index=True, nullable=False)
    description = Column(String)
    create_time = Column(Date)
    # avatar = Column(String, nullable=False)
    # video_url = Column(String, nullable=False)
    # is_follow = Column(Boolean, default=False)
    # like_num = Column(Integer, default=0)
    # collect_num = Column(Integer, default=0)
    # comment_num = Column(Integer, default=0)
    # share_num = Column(Integer, default=0)

    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="videos")
