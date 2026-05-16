from collections.abc import AsyncGenerator
from datetime import datetime
import uuid

from sqlalchemy import String, DateTime, Text
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


DATABASE_URL = "sqlite+aiosqlite:///./test.db"


class Base(DeclarativeBase):
    pass


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    caption: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    url: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    file_type: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    file_name: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )


engine = create_async_engine(
    DATABASE_URL,
    echo=True
)

async_session_maker = async_sessionmaker(
    engine,
    expire_on_commit=False
)


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session