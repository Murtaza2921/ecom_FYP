# app/services/user_service.py
from app.db.database import users_collection
from app.core.security import hash_password, verify_password, create_access_token
from bson.objectid import ObjectId
from app.models.user import UserResponse
from typing import Optional

def create_user(user_data):
    hashed_password = hash_password(user_data.password)
    user = {
        "email": user_data.email,
        "password": hashed_password,
        "is_admin": user_data.is_admin
    }
    result = users_collection.insert_one(user)
    return str(result.inserted_id)

def authenticate_user(email: str, password: str):
    user = users_collection.find_one({"email": email})
    if user and verify_password(password, user["password"]):
        return user
    return None

async def get_user_by_id(user_id: str) -> Optional[UserResponse]:
    user_data = users_collection.find_one({"_id": ObjectId(user_id)})
    if user_data:
        user_data["id"] = str(user_data["_id"])  # Convert ObjectId to string
        del user_data["_id"]  # Remove the MongoDB _id field
        return UserResponse(**user_data)
    return None