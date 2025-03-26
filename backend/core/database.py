import os 
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = os.getenv("MONGO_URL")
client = AsyncIOMotorClient(MONGO_URL)
db = client["mydatabase"]

# user collection
users_collection = db["users"]
diagnosis_collection = db["diagnosis"]
user_images_collection = db["user_images"]
