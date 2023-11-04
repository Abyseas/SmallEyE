import qiniu
from .CONST import access_key, secret_key, bucket_name


q = qiniu.Auth(access_key, secret_key)
bucket = qiniu.BucketManager(q)
bucket_domains = bucket.list_domains(bucket_name)
base_domain = f"http://{bucket_domains[0][0]}"


def before_upload_data(key: str):
    ret, info = bucket.stat(bucket_name, key)
    if ret is not None:
        bucket.delete(bucket_name, key)


def get_outbound_link(key: str):
    return q.private_download_url(f"{base_domain}/{key}")
