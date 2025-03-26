# app/main.py
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import diagnosis_routes, chat_routes, user_routes, upload_images
from image_processing import load_model_from_file

app = FastAPI()

# Cấu hình CORS (cho phép tất cả origins cho development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model khi khởi động ứng dụng
@app.on_event("startup")
def load_pretrained_model():
    model_path = os.path.join(os.path.dirname(__file__), "mobilenet_model.h5")
    try:
        app.state.model = load_model_from_file(model_path)
        print("Pre-trained model loaded successfully.")
    except Exception as e:
        print(f"Error loading pre-trained model: {e}")

app.include_router(diagnosis_routes.router, prefix="/api/diagnosis")
app.include_router(chat_routes.router, prefix="/api/chat")
app.include_router(user_routes.router, prefix="/api/users")
app.include_router(upload_images.router, prefix="/api/images")