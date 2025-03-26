from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from auth import get_current_user
from utils import upload_file_to_minio
import uuid, os
from database import user_images_collection
from datetime import datetime

router = APIRouter()

@router.post("/upload")
async def upload_image(file: UploadFile = File(...), current_user: dict = Depends(get_current_user)):
    # Lưu file tạm
    file_ext = file.filename.split(".")[-1]
    temp_filename = f"{uuid.uuid4()}.{file_ext}"
    temp_path = f"./temp/{temp_filename}"

    # Đảm bảo thư mục temp tồn tại
    os.makedirs("./temp", exist_ok=True)

    with open(temp_path, "wb") as f:
        content = await file.read()
        f.write(content)

    # Upload lên MinIO
    object_name = f"{current_user['_id']}/{temp_filename}"
    minio_url = upload_file_to_minio(temp_path, object_name)

    # Lưu metadata vào MongoDB
    doc = {
        "user_id": str(current_user["_id"]),
        "image_url": minio_url,
        "created_at": datetime.utcnow()
    }
    result = await user_images_collection.insert_one(doc)

    os.remove(temp_path)

    return {
        "success": True,
        "image_id": str(result.inserted_id),
        "image_url": minio_url
    }
    
@router.get("/my-images")
async def get_my_images(current_user: dict = Depends(get_current_user)):
    user_id = str(current_user["_id"])
    cursor = user_images_collection.find({"user_id": user_id})
    images = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        images.append(doc)
    return {"success": True, "data": images}