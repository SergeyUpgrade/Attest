import asyncio

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase

engine = create_async_engine("sqlite+aiosqlite://", echo=False)

async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session():
    async with async_session() as session:
        return session


class Base(AsyncAttrs, DeclarativeBase):
    pass


async def db_create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
