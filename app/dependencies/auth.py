# app/dependencies/auth.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from typing import Optional, Callable
#from app.core.config import settings
from app.services.user_service import get_user_by_id
from app.models.user import UserResponse
import logging
from dotenv import load_dotenv
import os

load_dotenv()
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")

def get_user_by_id_dependency() -> Callable:
    return get_user_by_id

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  # Token URL for authentication

logger = logging.getLogger(__name__)

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    get_user_by_id: Callable = Depends(get_user_by_id_dependency),  # Inject the function
) -> UserResponse:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        logger.info(f"Decoding token: {token}")
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        logger.info(f"Token payload: {payload}")
        user_id: Optional[str] = payload.get("user_id")
        if user_id is None:
            logger.error("Token missing 'sub' claim")
            raise credentials_exception
    except JWTError as e:
        logger.error(f"JWTError: {e}")
        raise credentials_exception

    logger.info(f"Fetching user with ID: {user_id}")
    user = await get_user_by_id(user_id)
    if user is None:
        logger.error(f"User not found for ID: {user_id}")
        raise credentials_exception

    return UserResponse(**user.dict())  # Convert to Pydantic model