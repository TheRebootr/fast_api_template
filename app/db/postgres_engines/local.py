from typing import Callable

from sqlalchemy import Engine, create_engine
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    create_async_engine,
)
from sqlalchemy.pool import NullPool

from app.config import config


def get_async_engine() -> AsyncEngine:
    """Create and configure async database engine with connection pooling."""

    return create_async_engine(
        config.DATABASE_URL,
        echo=config.DATABASE_ECHO,
        poolclass=None,
    )


def get_engine() -> Engine:
    """Create synchronous engine for alembic migrations (if needed).

    Note: This is a synchronous engine and should be used cautiously
    in an async application to avoid blocking the event loop.

    """
    # Use NullPool for synchronous engine to avoid connection issues
    return create_engine(
        config.DATABASE_URL.replace("asyncpg", "psycopg2"),
        connect_args={"connect_timeout": 15},
        echo=config.DATABASE_ECHO,
        poolclass=NullPool,
    )


get_local_async_engine: Callable[[], AsyncEngine] = get_async_engine
get_local_engine: Callable[[], Engine] = get_engine
