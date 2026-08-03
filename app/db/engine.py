from typing import Optional
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, async_sessionmaker

engine: Optional[AsyncEngine] = None
AsyncSessionLocal: Optional[async_sessionmaker] = None


def init_db(
    db_username: str,
    db_password: str,
    db_host: str,
    db_port: int,
    db_name: str,
    *,
    echo: bool = True,
    pool_size: int = 10,
    max_overflow: int = 20,
    pool_timeout: int = 30,
    pool_recycle: int = 1800,
    pool_pre_ping: bool = True,
): 
    global engine, AsyncSessionLocal

    db_url = URL.create(
        drivername="postgresql+asyncpg",
        username=db_username,
        password=db_password,
        host=db_host,
        port=db_port,
        database=db_name,
    )

    engine = create_async_engine(
        url=db_url,
        echo=echo,
        pool_size=pool_size,
        max_overflow=max_overflow,
        pool_timeout=pool_timeout,
        pool_recycle=pool_recycle,
        pool_pre_ping=pool_pre_ping,
    )

    AsyncSessionLocal = async_sessionmaker(
        bind=engine, expire_on_commit=False, autoflush=False
    )


def get_engine() -> AsyncEngine:
    if engine is None:
        raise RuntimeError("Database engine not initialized. Call init_db() first.")
    return engine


def get_sessionmaker() -> async_sessionmaker:
    if AsyncSessionLocal is None:
        raise RuntimeError("Sessionmaker not initialized. Call init_db() first.")
    return AsyncSessionLocal


async def dispose_db() -> None: 
    if engine is not None:
        await engine.dispose()