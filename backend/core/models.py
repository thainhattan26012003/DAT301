from pydantic import BaseModel, Field
from typing import Optional

class UserCreate(BaseModel):
    username: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class ImageMetadata(BaseModel):
    id: Optional[str]
    user_id: str
    image_url: str
    diagnosis_result: Optional[str] = None
    confidence: Optional[float] = None
    created_at: Optional[str] = None