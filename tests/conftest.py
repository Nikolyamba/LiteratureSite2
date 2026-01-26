import uuid

import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from backend.database.base import Base
from backend.models.user import UserRole

DATABASE_URL = "sqlite+aiosqlite:///./test.db"

test_engine = create_async_engine(DATABASE_URL, echo=True, future=True)

TestingSessionLocal = async_sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_test_db():
    async with TestingSessionLocal() as session:
        yield session

@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

class FakeUser:
    id: uuid.UUID = '123ABC'
    login: str = 'Hype'
    hashed_password: str = '1234qwer'
    email: str = '1'
    image: None
    role: UserRole.user
    info: None

class FakeAdmin:
    id: uuid.UUID = '231BDC'
    login: str = 'Pro'
    hashed_password: str = '1234qwera'
    email: str = '2'
    image: None
    role: UserRole.admin
    info: None