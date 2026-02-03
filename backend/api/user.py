import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.concurrency import run_in_threadpool

from backend.database.session import get_db
from backend.features.check_pass import check_password
from backend.features.rights import can_edit_user
from backend.features.auth import create_access_token, create_refresh_token, get_current_user, decode_token
from backend.features.hash_pass import hash_password, verify_password
from backend.models import User

from backend.redis_dir.redis_config import get_redis
from backend.schemas.user import UserRegister, LoginSchema, GetAllUsers, UserInfo, EditUserData

u_router = APIRouter(prefix='/users')


@u_router.post('')
async def register(data: UserRegister, db: AsyncSession = Depends(get_db)) -> dict:
    q = select(User).where((User.login == data.login) | (User.email == data.email))
    result = await db.execute(q)
    old_user = result.scalar_one_or_none()
    if old_user:
        raise HTTPException(status_code=409, detail='Такой логин или email уже используются на сайте')

    if not await check_password(data.password):
        raise HTTPException(status_code=401, detail='Пароль должен содержать буквы и цифры')

    password_hash = await run_in_threadpool(
        hash_password,
        data.password
    )

    new_user = User(login=data.login,
                    hashed_password=password_hash,
                    email=data.email,
                    role=data.role,
                    image=data.image,
                    info=data.info)

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return {'success': True, 'new_user': f'{new_user.login}'}


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
    await r.delete(f'refresh:{jti_id}')

    return {'success': True, 'msg': f'{current_user.login} вышел из системы'}


@u_router.post('/refresh')
async def get_new_access_token(refresh_token: str) -> dict:
    payload = decode_token(refresh_token)

    if payload.get("type") != "refresh_token":
        raise HTTPException(401, "Неверный тип токена")

    jti = payload.get("jti")
    r = get_redis()
    if not r.exists(f"refresh:{jti}"):
        raise HTTPException(status_code=401, detail="Refresh токен недействителен")

    user_login = await r.get(f"refresh:{jti}")
    await r.delete(f"refresh:{jti}")

    new_access_token = create_access_token(user_login)
    new_refresh_token = create_refresh_token(user_login)
    return {"success": True, "payload": {'access_token': new_access_token, 'refresh_token': new_refresh_token}}


@u_router.get('', response_model=List[GetAllUsers])
async def get_all_users(db: AsyncSession = Depends(get_db)):
    q = select(User)
    result = await db.execute(q)
    users = result.scalars().all()
    return users


@u_router.get('/{user_id}', response_model=UserInfo)
async def get_user(user_id: uuid.UUID, db: AsyncSession = Depends(get_db),
                   current_user: User = Depends(get_current_user)):
    q = select(User).where(User.id == user_id)
    result = await db.execute(q)
    target_user = result.scalar_one_or_none()

    return target_user


@u_router.delete('/{user_id}')
async def del_user(user_id: uuid.UUID, db: AsyncSession = Depends(get_db),
                   current_user: User = Depends(get_current_user)) -> dict:
    q = select(User).where(User.id == user_id)
    result = await db.execute(q)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail='Пользователь не найден')

    if not can_edit_user(current_user, user):
        raise HTTPException(status_code=403, detail='У вас нет прав доступа')

    await db.delete(user)
    await db.commit()

    return {'status': 'deleted'}


# FIXME сделать пароль

@u_router.patch('/{user_id}', response_model=UserInfo)
async def edit_user(user_id: uuid.UUID, data: EditUserData,
                    db: AsyncSession = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    q = select(User).where(User.id == user_id)
    result = await db.execute(q)
    target_user = result.scalar_one_or_none()

    if not target_user:
        raise HTTPException(status_code=404, detail='Пользователь не найден')

    if not can_edit_user(current_user, target_user):
        raise HTTPException(status_code=403, detail='У вас нет прав доступа')

    update_data = data.model_dump(exclude_unset=True)

    for row, info in update_data.items():
        setattr(target_user, row, info)

    await db.commit()
    await db.refresh(target_user)
