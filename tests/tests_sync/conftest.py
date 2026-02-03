import pytest

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from backend.database.base import Base
from starlette.testclient import TestClient

from backend.features.auth import get_current_user
from backend.main import app
from backend.models import User
from backend.models.user import UserRole

client = TestClient(app)

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:" #вопрос, :memory или создавать test.db?

test_engine = create_async_engine(TEST_DATABASE_URL, echo=False, future=True)

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


@pytest.fixture
async def db_session():
    async with TestingSessionLocal() as session:
        yield session
        await session.rollback()


@pytest.fixture
async def fake_normal_user(db_session):
    user = User(id = '123qwe',
                login = '123qwe',
                password = '1234qwer',
                email = '123qwe',
                role = UserRole.user)
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest.fixture
async def fake_admin_user(db_session):
    admin = User(id='124qwe',
                login='124qwe',
                password='1234qwer',
                email='124qwe',
                role=UserRole.admin)
    db_session.add(admin)
    await db_session.commit()
    await db_session.refresh(admin)
    return admin


@pytest.fixture
def override_current_admin(fake_admin_user):
    def _override():
        return fake_admin_user
    app.dependency_overrides[get_current_user] = _override
    yield
    app.dependency_overrides = {}

@pytest.fixture
def override_current_user(fake_normal_user):
    def _override():
        return fake_normal_user
    app.dependency_overrides[get_current_user] = _override()
    yield
    app.dependency_overrides = {}
