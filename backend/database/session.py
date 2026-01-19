import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

load_dotenv()

DATABASE_URL = os.getenv('DB_URL')

async_engine = create_async_engine(DATABASE_URL, echo=True, future=True)
engine = create_engine(DATABASE_URL)

AsyncSessionLocal = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

SessionLocal = sessionmaker(bind=engine)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session