import os
from dotenv import load_dotenv
load_dotenv()
from service_config import minio_client
from minio.error import S3Error
from service_config import MINIO_BUCKET

MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT")

def upload_file_to_minio(file_path: str, object_name: str) -> str:
    # Tạo bucket nếu chưa có
    found = minio_client.bucket_exists(MINIO_BUCKET)
    if not found:
        minio_client.make_bucket(MINIO_BUCKET)
    try:
        minio_client.fput_object(MINIO_BUCKET, object_name, file_path)
        # Tạo URL trả về (nếu bucket public)
        url = f"http://{MINIO_ENDPOINT}/{MINIO_BUCKET}/{object_name}"
        return url
    except S3Error as e:
        print("Error uploading to minio:", e)
        raise e

