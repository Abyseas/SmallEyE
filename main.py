from typing import Union, Dict
from fastapi import FastAPI
from pydantic import BaseModel
import qiniu

# FastAPI application
app = FastAPI()

access_key = "x34GCNDuYpCFsNtqkrri3Eagr6OANYyboWRZtWQv"
secret_key = "f_lfzdkBoEfOa_7a_0yrMOcIdfr-cHv9H463B5Xh"
q = qiniu.Auth(access_key, secret_key)
bucket = qiniu.BucketManager(q)


class BucketUploadArgs(BaseModel):
    key: str
    file_path: str
    metadata: Dict[str, Union[str, int]] = None


@app.get("/")
def read_root():
    return "Hello FastAPI"


@app.get("/list/{bucket_name}")
def read_bucket_file_list(bucket_name: str, prefix: Union[str] = None, marker: Union[str] = None,
                          limit: Union[int] = None, delimiter: Union[str] = None):
    ret, eof, info = bucket.list(bucket_name, prefix, marker, limit, delimiter)
    marker = ret.get("marker")
    return ret, marker


@app.post("/upload/video/{bucket_name}")
def upload_short_video(bucket_name: str, args: BucketUploadArgs):
    token = q.upload_token(bucket_name)
    ret, info = qiniu.put_file(token, **args.model_dump())
    return ret

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}
