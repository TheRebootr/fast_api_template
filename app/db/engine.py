"""Async database engine configuration and lifecycle management."""

from loguru import logger
from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_sessionmaker,
)

from app.config import PostgresType, config
from app.db.postgres_engines.databricks import get_databricks_async_engine
from app.db.postgres_engines.local import get_local_async_engine

# Global engine instance (initialized at startup)
engine: AsyncEngine | None = None

# Global session factory (initialized at startup)
AsyncSessionLocal: async_sessionmaker | None = None


def get_engine() -> AsyncEngine:
    """Create and configure async database engine based on POSTGRES_PROVIDER.

    Dynamically imports and uses the appropriate postgres engine based on
    the POSTGRES_PROVIDER configuration setting.
    """
    provider = config.POSTGRES_PROVIDER

    if provider == PostgresType.LOCAL:
        return get_local_async_engine()
    elif provider == PostgresType.DATABRICKS:
        if get_databricks_async_engine is None:
            raise ValueError(
                "Databricks engine is not configured. "
                "Please implement the databricks connector."
            )
        return get_databricks_async_engine
    else:
        raise ValueError(
            f"Invalid POSTGRES_PROVIDER: {config.POSTGRES_PROVIDER}. "
            f"Supported providers: local, databricks"
        )


def create_session_factory(
    engine: AsyncEngine,
) -> async_sessionmaker:
    """Create session factory bound to engine.

    Session Configuration:
    - expire_on_commit=False: Keep objects accessible after commit
    - autoflush=True: Flush changes before queries
    - autocommit=False: Require explicit commit

    Args:
        engine: The database engine to bind sessions to

    Returns:
        Session factory for creating AsyncSession instances
    """
    return async_sessionmaker(
        engine,
        expire_on_commit=False,
        autoflush=True,
        autocommit=False,
    )


async def init_db() -> None:
    """Initialize database engine and session factory.

    Called during application startup (lifespan context).
    Sets global `engine` and `AsyncSessionLocal` variables.
    Logs connection establishment.
    """
    global engine, AsyncSessionLocal

    try:
        logger.info("...Initializing Database...")
        engine = get_engine()
        AsyncSessionLocal = create_session_factory(engine)
        logger.info(f"(DB Provider: {config.POSTGRES_PROVIDER})")
    except Exception as exc:
        logger.error(
            f"Failed to initialize database connection: "
            f"{exc.__class__.__name__}: {exc}"
        )
        raise


async def dispose_db() -> None:
    """Dispose database engine and close all connections.

    Called during application shutdown (lifespan context).
    Ensures clean shutdown with no connection leaks.
    Logs connection closure.
    """
    global engine, AsyncSessionLocal

    if engine is not None:
        try:
            logger.info("...Closing Database...")
            await engine.dispose()
            logger.info("Database connections closed successfully")
        except Exception as exc:
            logger.error(
                f"Error while disposing database engine: "
                f"{exc.__class__.__name__}: {exc}"
            )
        finally:
            engine = None
            AsyncSessionLocal = None
    else:
        logger.debug("Database engine already disposed or not initialized")


async def check_db_health() -> bool:
    """Check database connectivity."""
    global engine

    if engine is None:
        return False

    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        return True
    except Exception as exc:
        logger.error(f"Database health check failed: {exc}")
        return False
