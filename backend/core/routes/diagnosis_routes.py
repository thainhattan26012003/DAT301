from fastapi import APIRouter, UploadFile, File, HTTPException, Request
from image_processing import predict_diagnosis
from datetime import datetime
import io, uuid, os

router = APIRouter()

ALLOWED_EXTENSIONS = (".png", ".jpg", ".jpeg")

def validate_image_file(file: UploadFile):
    filename = file.filename.lower()
    if not any(filename.endswith(ext) for ext in ALLOWED_EXTENSIONS):
        raise HTTPException(
            status_code=400,
            detail="File ảnh không hợp lệ. Chỉ hỗ trợ các định dạng: png, jpg, jpeg."
        )

@router.post("/pretrained")
async def diagnose_pretrained(request: Request, image_file: UploadFile = File(...)):
    try:
        validate_image_file(image_file)
        image_bytes = await image_file.read()
        model = request.app.state.model
        if model is None:
            raise HTTPException(status_code=500, detail="Model chưa được load.")
        result = predict_diagnosis(model, image_bytes)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
