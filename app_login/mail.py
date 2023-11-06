from datetime import timedelta
import socket

import yagmail

from . import create_access_token
from app_utils.CONST import ACCESS_TOKEN_EXPIRE_MINUTES


mail_user = "abyseas@163.com"
mail_password = "LTLQCBZOVPOGTHGH"
mail_host = "smtp.163.com"

yag = yagmail.SMTP(mail_user, mail_password, mail_host)
yag.useralias = "SmallEye"


def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


def send_token(to: str, username: str, password: str, url: str):
    to_encode = {
        "username": username,
        "password": password
    }
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(to_encode, access_token_expires)
    # ip = get_host_ip()
    # validate_url = f"http://{ip}:8000/{url}/{access_token}
    validate_url = f"{url}/{access_token}"
    contents = f"""
    Hello {username}, please click this {validate_url} to activate your account, thanks for register!
    """
    yag.send(to, 'Activate your account', contents)
    return access_token
