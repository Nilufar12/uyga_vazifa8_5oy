import os
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

DB_URL = 'sqlite+aiosqlite:///./main'

engine = create_async_engine(DB_URL)
LocalSession = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_db():
    async with LocalSession() as session:
        yield session


MEDIA_DIR = 'media'
os.makedirs(MEDIA_DIR, exist_ok=True)