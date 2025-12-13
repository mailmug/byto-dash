from collections.abc import AsyncGenerator

from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, relationship

from app.core.config import settings
from app.models.base import Base
from app.models.base import Base

class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "users"
    
    posts = relationship("Post", back_populates="user", cascade="all, delete-orphan")



