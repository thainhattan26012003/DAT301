from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from chat import rag_flow

router = APIRouter()

class ChatRequest(BaseModel):
    question: str
    diagnosis: str  # chuỗi chứa kết quả dự đoán từ ảnh

@router.post("/chat")
async def chat_endpoint(chat_request: ChatRequest):
    try:
        answer = await rag_flow(chat_request.question, chat_request.diagnosis)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
