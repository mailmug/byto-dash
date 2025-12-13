from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from app.models.user import Base
from app.core.config import settings
from collections.abc import AsyncGenerator

from app.models.base import Base

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.core.config import settings

# Async engine 
engine = create_async_engine(settings.DATABASE_URL, echo=True)

# Async session
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

# Create tables (async)
async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Dependency for FastAPI routes
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session