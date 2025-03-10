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


class UserBase(BaseModel):
    email: EmailStr
    is_admin: bool

class UserInDB(UserBase):
    id: str  # This will be the string representation of the ObjectId

class UserResponse(BaseModel):
    id: str
    email: EmailStr
    is_admin: bool

    # class Config:
    #     json_encoders = {ObjectId: str}  # Handle ObjectId serialization