from minio import Minio
from minio.error import S3Error
from backend.app.core.config import settings
import os

client = Minio(
    settings.MINIO_ENDPOINT,
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=False,
)

def ensure_bucket(bucket: str):
    if not client.bucket_exists(bucket):
        client.make_bucket(bucket)

def upload_file(local_path: str, bucket: str, object_name: str):
    ensure_bucket(bucket)
    client.fput_object(bucket, object_name, local_path)
    return f"s3://{bucket}/{object_name}"

def get_presigned_url(uri: str, expiry: int = 3600) -> str:
    # uri: s3://bucket/object
    parts = uri.replace("s3://", "").split("/", 1)
    bucket, object_name = parts[0], parts[1]
    return client.presigned_get_object(bucket, object_name, expires=expiry)
