import qiniu
from CONST import access_key, secret_key


q = qiniu.Auth(access_key, secret_key)
bucket = qiniu.BucketManager(q)


def before_upload_data(bucket_name: str, key: str):
    ret, info = bucket.stat(bucket_name, key)
    if ret is not None:
        bucket.delete(bucket_name, key)
