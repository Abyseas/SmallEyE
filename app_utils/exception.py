from typing import Union, Optional
from enum import IntEnum


class ExceptionCode(IntEnum):
    # user relate
    EMAIL_ALREADY_EXIST = 1001
    USER_NOT_FOUND = 1002
    INCORRECT_USER_OR_PASSWORD = 1003
    CREDENTIALS_NOT_VALIDATE = 1004
    USER_NOT_ACTIVE = 1005
    NO_AUTHENTICATE = 1006  # 请求未带 authenticate头

    # video relate
    VIDEO_NOT_FOUND = 1011


class ResException(Exception):
    def __init__(self, code: Union[ExceptionCode, int], error: str,
                 headers: Optional[dict[str, str]] = None):
        self.code = code
        self.error = error
        self.headers = headers
