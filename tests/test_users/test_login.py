from fastapi.concurrency import run_in_threadpool
import pytest
from sqlalchemy import select

from backend.features.hash_pass import verify_password
from backend.models.user import User


@pytest.mark.asyncio
async def test_login_success(async_client, db_session, fake_normal_user):
    payload = {"login": fake_normal_user.login,
               "password": fake_normal_user.plain_password,
               }
    response = await async_client.post('/api/users/login', json=payload)
    assert response.status_code == 200

    data = response.json()
    assert 'access_token' in data
    assert 'refresh_token' in data

    result = await db_session.execute(select(User).where(User.login == payload['login']))
    user = result.scalar_one_or_none()
    assert user.login == data['login']
    assert await run_in_threadpool(verify_password, payload['password'], user.hashed_password)
    