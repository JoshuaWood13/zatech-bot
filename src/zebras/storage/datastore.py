from __future__ import annotations

from typing import Optional
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine


def create_engine(database_url: str) -> AsyncEngine:
    """Create an async SQLAlchemy engine for Postgres.

    Use a Postgres DSN with asyncpg driver, e.g.,
    postgresql+asyncpg://user:password@host:5432/dbname
    Neon Postgres works by using its provided DSN.
    """

    return create_async_engine(database_url, pool_pre_ping=True, pool_size=5, max_overflow=5)

