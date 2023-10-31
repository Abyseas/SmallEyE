# built-in and 3rd
from typing import Union, Dict, Any
import time
import json
import requests
from aux_tools import q, bucket, before_upload_data

# fastAPI
import uvicorn
from fastapi import FastAPI, Form, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# qi niu yun
import qiniu

# FastAPI application
app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


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
    bucket_domains = bucket.list_domains(bucket_name)
    base_domain = f"http://{bucket_domains[0][0]}"
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
    before_upload_data(bucket_name, key)
    ret, info = qiniu.put_data(token, key, file_bytes)
    meta_key = f"user@{user_id}/manifest/{media_type}/{title}.json"
    before_upload_data(bucket_name, meta_key)
    qiniu.put_data(token, meta_key, metadata)

    return ret


@app.get("/get_metadata/{bucket_name}/{filename}")
def read_file_metadata(bucket_name: str, filename: str):
    key = f"user2/video/{filename}"
    ret, info = bucket.stat(bucket_name, key)

    return ret


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
