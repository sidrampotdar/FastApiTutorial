import asyncio
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from alembic import context
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.core.config import settings
from app.db.base import Base

config = context.config
fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_online() -> None:
    connectable = create_async_engine(
        settings.DATABASE_URL,
        future=True,
        echo=False,
        pool_pre_ping=True,
    )

    async def do_run_migrations(connection: Connection) -> None:
        context.configure(connection=connection, target_metadata=target_metadata, compare_type=True)
        with context.begin_transaction():
            context.run_migrations()

    async def async_main() -> None:
        async with connectable.connect() as connection:
            await connection.run_sync(do_run_migrations)

    asyncio.run(async_main())


if context.is_offline_mode():
    raise RuntimeError("Offline migrations are not supported in this configuration.")
else:
    run_migrations_online()
