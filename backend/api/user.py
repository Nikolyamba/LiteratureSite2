import uuid
from typing import Optional, Annotated, List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.concurrency import run_in_threadpool

from backend.database.session import get_db
from backend.features.admin_func import can_delete_user
from backend.features.auth import create_access_token, create_refresh_token, get_current_user, decode_token
from backend.features.hash_pass import hash_password, verify_password
from backend.models import User
from backend.models.user import UserRole
from backend.redis_dir.redis_config import get_redis

u_router = APIRouter(prefix='/users')

class UserRegister(BaseModel):
    login: str
    password: Annotated[str, Field(min_length=8, max_length=128)]
    email: str
    image: Optional[str | None] = None
    info: Optional[str | None] = None

@u_router.post('')
async def register(data: UserRegister, db: AsyncSession = Depends(get_db)) -> dict:
    q = select(User).where((User.login == data.login) | (User.email == data.email))
    result = await db.execute(q)
    old_user = result.scalar_one_or_none()
    if old_user:
        raise HTTPException(status_code=409, detail='Такой логин или email уже используются на сайте')

    password_hash = await run_in_threadpool(
        hash_password,
        data.password
    )

    new_user = User(login = data.login,
                    hashed_password = password_hash,
                    email = data.email,
                    role = UserRole.user,
                    image = data.image,
                    info = data.info)

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return {'success': True, 'new_user': f'{new_user.login}'}

class LoginSchema(BaseModel):
    login: str
    password: str

@u_router.post('/login')
async def login(data: LoginSchema, db: AsyncSession = Depends(get_db)) -> dict:
    user = await db.scalar(
        select(User).where(User.login == data.login)
    )

    if not user or not await run_in_threadpool(verify_password, data.password, user.hashed_password):
        raise HTTPException(401, 'Неверный логин или пароль')

    access_token = create_access_token(user.login)
    refresh_token = await create_refresh_token(user.login)

    return {'access_token': access_token, 'refresh_token': refresh_token}

@u_router.post('/logout')
async def logout(refresh_token: str, current_user: User = Depends(get_current_user)) -> dict:
    payload = decode_token(refresh_token)
    jti_id = payload.get('jti')
    r = get_redis()
    await r.delete(f'refresh{jti_id}')

    return {'success': True, 'msg': f'{current_user.login} вышел из системы'}

@u_router.post('/refresh')
async def get_new_access_token(refresh_token: str) -> dict:
    payload = decode_token(refresh_token)

    jti = payload.get("jti")
    r = get_redis()
    if not r.exists(f"refresh:{jti}"):
        raise HTTPException(status_code=401, detail="Refresh токен недействителен")

    login = r.get("sub")

    new_access_token = create_access_token(login)
    return {"success": True, "access_token": new_access_token}

class GetAllUsers(BaseModel):
    login: str
    image: Optional[str | None] = None
    class Config:
        orm_mode = True

@u_router.get('', response_model=List[GetAllUsers])
async def get_all_users(db: AsyncSession = Depends(get_db)):
    q = select(User)
    result = await db.execute(q)
    users = result.scalars().all()
    return users

@u_router.delete('/{user_id}')
async def del_user(user_id: uuid.UUID, db: AsyncSession = Depends(get_db),
                   current_user: User = Depends(get_current_user)) -> dict:
    q = select(User).where(User.id == user_id)
    result = await db.execute(q)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail='Пользователь не найден')

    if not can_delete_user(current_user, user):
        raise HTTPException(status_code=403, detail='У вас нет прав доступа')

    await db.delete(user)
    await db.commit()

    return {'status': 'deleted'}


