# import uuid
#
# import pytest
# from httpx import AsyncClient
# from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
#
# from backend.database.base import Base
# from backend.database.session import get_db
# from backend.main import app
# from backend.models.user import UserRole
#
# DATABASE_URL = "sqlite+aiosqlite:///./test.db"
#
# test_engine = create_async_engine(DATABASE_URL, echo=False, future=True)
#
# TestingSessionLocal = async_sessionmaker(
#     test_engine,
#     class_=AsyncSession,
#     expire_on_commit=False,
# )
#
# async def get_test_db():
#     async with TestingSessionLocal() as session:
#         yield session
#
# @pytest.fixture(scope="session", autouse=True)
# async def prepare_database():
#     async with test_engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#     yield
#     async with test_engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#
# class FakeUser:
#     id: uuid.UUID = '2321bdsad'
#     login: str = 'Test'
#     hashed_password: str = '1231qwewqe'
#     email: str = '2313'
#     image: None
#     role: UserRole.user
#     info: None
#
# class FakeAdmin:
#     id: uuid.UUID = '231BDC'
#     login: str = 'Pro'
#     hashed_password: str = '1234qwera'
#     email: str = '2'
#     image: None
#     role: UserRole.admin
#     info: None
#
# app.dependency_overrides[get_db] = get_test_db
#
# @pytest.fixture
# async def client():
#     async with AsyncClient(app=app, base_url="http://test") as ac:
#         yield ac
from starlette.testclient import TestClient

from backend.main import app

client = TestClient(app)