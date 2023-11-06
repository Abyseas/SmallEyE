from enum import Enum

from pydantic import BaseModel


class VideoCategoryType(Enum):
    DEFAULT = "no classify"
    TECH = "tech"
    FOOD = "food"
    MOVIE = "movie"
    GAME = "game"
    KNOWLEDGE = "knowledge"
    NEWS = "news"
    MUSIC = "music"
    FASHION = "fashion"
    LIFE = "life"
    SPORT = "sport"

    def __int__(self, value: str):
        self.value = value
