import pytest
from sqlalchemy import and_, select

from backend.models.user import User


@pytest.mark.asyncio
async def test_register_success(async_client, db_session):
    payload = {"login": "Justice",
               "email": "qwerty@.com",
               "password": "abra1234",
               }
    response = await async_client.post('/api/users/register', json=payload)
    assert response.status_code == 200

    data = response.json()
    assert data.get('success') == True
    
    result = await db_session.execute(select(User).where(and_(User.login == payload['login'],
                                              User.email == payload['email'])))
    user = result.scalar_one_or_none()
    
    assert user is not None
    assert isinstance(user, User)

@pytest.mark.asyncio
async def test_register_fail_login_or_email(async_client, override_db_dependency, fake_normal_user):
    """
    Этот тест находит пользователя с таким логином или email и возвращает ошибку
    """
    payload = {"login": "123qwe",
               "email": "123qwe",
               "password": "abra1234",
               }
    response = await async_client.post('/api/users/register', json=payload)
    assert response.status_code == 401

    data = response.json()
    assert data.get('detail') == 'Такой логин или email уже используются на сайте'

@pytest.mark.asyncio
async def test_register_fail_pass(async_client, db_session):
    """
    Этот тест возвращает ошибку регистрации из-за некорректного пароля
    """
    payload = {"login": "123445qwewqe",
               "email": "qwertsssy@.com",
               "password": "abrababa",
               }
    response = await async_client.post('/api/users/register', json=payload)
    assert response.status_code == 401

    data = response.json()
    assert data.get('detail') == 'Пароль должен содержать буквы и цифры'

    result = await db_session.execute(select(User).where(and_(User.login == payload['login'],
                                              User.email == payload['email'])))
    user = result.scalar_one_or_none()
    
    assert user is None