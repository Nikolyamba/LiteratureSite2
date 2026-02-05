import uuid
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from backend.database.base import Base
from backend.database.session import get_db
from backend.features.auth import get_current_user
from backend.main import app
from backend.models import User
from backend.models.genre import Genre
from backend.models.user import UserRole

TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

test_engine = create_async_engine(TEST_DATABASE_URL, echo=False, future=True)

TestingSessionLocal = async_sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session


@pytest.fixture(autouse=True)
def override_db_dependency(db_session):
    async def _override():
        yield db_session

    app.dependency_overrides[get_db] = _override
    yield
    app.dependency_overrides.clear()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_database():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def async_client():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        yield client


@pytest.fixture
async def db_session():
    async with test_engine.connect() as conn:
        trans = await conn.begin()
        session = AsyncSession(bind=conn, expire_on_commit=False)
        try:
            yield session
        finally:
            await session.close()
            await trans.rollback()


@pytest.fixture
async def fake_normal_user(db_session):
    user = User(
        id=uuid.uuid4(),
        login='123qwe',
        hashed_password='1234qwer',
        email='123qwe',
        role=UserRole.user
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest.fixture
async def fake_admin_user(db_session):
    admin = User(
        id=uuid.uuid4(),
        login='124qwe',
        hashed_password='1234qwer',
        email='124qwe',
        role=UserRole.admin
    )
    db_session.add(admin)
    await db_session.commit()
    await db_session.refresh(admin)
    return admin


@pytest.fixture
async def fake_genre(db_session):
    genre = Genre(
        id=uuid.uuid4(),
        genre_name='Detective',
        image='',
        description=''
    )
    db_session.add(genre)
    await db_session.flush()
    await db_session.refresh(genre)
    return genre


@pytest.fixture
async def override_current_admin(fake_admin_user):
    async def _override():
        return fake_admin_user

    app.dependency_overrides[get_current_user] = _override
    yield
    app.dependency_overrides.clear()


@pytest.fixture
async def override_current_user(fake_normal_user):
    async def _override():
        return fake_normal_user

    app.dependency_overrides[get_current_user] = _override
    yield
    app.dependency_overrides.clear()