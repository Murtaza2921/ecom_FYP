from fastapi import APIRouter, HTTPException, Depends
from app.models.user import UserCreate, UserLogin
from app.services.user_service import create_user, authenticate_user
from app.core.security import create_access_token
from datetime import timedelta

router = APIRouter()

@router.post("/signup")
def signup(user: UserCreate):
    user_id = create_user(user)
    return {"message": "User created", "user_id": user_id}

@router.post("/signin")
def signin(login_data: UserLogin):
    user = authenticate_user(login_data.email, login_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = create_access_token({"sub": user["email"]}, timedelta(hours=1))
    return {"access_token": token, "token_type": "bearer"}
