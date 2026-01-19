import os
import uuid
from datetime import datetime, timedelta

import jwt
from dotenv import load_dotenv
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.exceptions import HTTPException

from backend.database.session import get_db
from backend.models import User
from backend.redis.redis_config import redis_client

load_dotenv()

SECRET_KEY = os.getenv("KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15

def create_access_token(login: str):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": login,
        "type": "access_token",
        "exp": expire
    }
    access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return access_token

def create_refresh_token(login: str):
    jti = str(uuid.uuid4())
    expire = datetime.utcnow() + timedelta(days=30)
    payload = {
        "sub": login,
        "jti": jti,
        "type": "refresh_token",
        "exp": expire
    }
    refresh_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    redis_client.setex(f"refresh:{jti}", timedelta(days=30), login)
    return refresh_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def decode_token(token: str):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload

def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось получить текущего пользователя",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        login: int = payload.get("sub")
        if login is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    async with db.begin():
        result = await db.execute(select(User).where(User.login == login))
        user = result.scalar_one_or_none()
        if user is None:
            raise credentials_exception
    return user