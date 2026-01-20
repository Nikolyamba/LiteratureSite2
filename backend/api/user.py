from typing import Optional, Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.concurrency import run_in_threadpool

from backend.database.session import get_db
from backend.features.auth import create_access_token, create_refresh_token
from backend.features.hash_pass import hashed_password
from backend.models import User
from backend.models.user import UserRole

u_router = APIRouter(prefix='users')

class UserRegister(BaseModel):
    login: str
    password: Annotated[str, Field(min_length=8, max_length=128)]
    email: str
    info: Optional[str | None] = None

@u_router.post('')
async def register(data: UserRegister, db: AsyncSession = Depends(get_db)) -> dict:
    q = select(User).where((User.login == data.login) | (User.email == data.email))
    result = await db.execute(q)
    old_user = result.scalar_one_or_none()
    if old_user:
        raise HTTPException(status_code=409, detail='Такой логин или email уже используются на сайте')

    password_hash = await run_in_threadpool(
        hashed_password,
        data.password
    )

    new_user = User(login = data.login,
                    password = password_hash,
                    email = data.email,
                    role = UserRole.user.value,
                    info = data.info)

    async with db.begin():
        db.add(new_user)
        # TODO: ДОДЕЛАТЬ

    access_token = create_access_token(new_user.login)
    refresh_token = await create_refresh_token(new_user.login)

    return {'access_token': access_token, 'refresh_token': refresh_token}



