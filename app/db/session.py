
from sqlalchemy.ext.asyncio import AsyncSession
from collections.abc import AsyncGenerator

from .engine import get_sessionmaker


async def get_async_db_session() -> AsyncGenerator[AsyncSession, None]: 
    SessionLocal = get_sessionmaker()
    async with SessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise