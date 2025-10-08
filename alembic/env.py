"""Alembic environment configuration for async SQLAlchemy."""

from logging.config import fileConfig

from sqlalchemy import Engine
from sqlalchemy.engine import Connection

# Import all models to ensure they're registered with Base.metadata
# This is CRITICAL for Alembic autogenerate to detect model changes
import app.models  # noqa: F401
from alembic import context
from app.config import PostgresType
from app.config import config as app_config
from app.db.base import Base
from app.db.postgres_engines.databricks import get_databricks_engine
from app.db.postgres_engines.local import get_local_engine

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Override sqlalchemy.url from app configuration
# Use app_config to ensure .env file is properly loaded via pydantic-settings
config.set_main_option(
    "sqlalchemy.url", app_config.DATABASE_URL.replace("asyncpg", "psycopg2")
)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,  # Detect column type changes
        compare_server_default=True,  # Detect default value changes
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """Execute migrations with provided connection."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,  # Detect column type changes
        compare_server_default=True,  # Detect default value changes
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode (synchronous version)."""
    # Determine which engine to use based on POSTGRES_PROVIDER
    engine: Engine | None = (
        get_databricks_engine
        if app_config.POSTGRES_PROVIDER == PostgresType.DATABRICKS
        else get_local_engine()
    )

    if engine is None:
        raise ValueError("Engine is not configured properly.")

    with engine.connect() as connection:
        do_run_migrations(connection)
    engine.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
