from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    is_admin: bool = False

class UserResponse(BaseModel):
    id: str
    email: EmailStr
    is_admin: bool

class UserLogin(BaseModel):
    email: EmailStr
    password: str
