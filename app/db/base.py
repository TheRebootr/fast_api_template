"""SQLAlchemy declarative base and common model functionality."""

import uuid
from datetime import UTC, datetime

from sqlalchemy import MetaData
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declarative_mixin,
    mapped_column,
)

# Naming convention for constraints (PostgreSQL and Alembic best practice)
convention = {
    "ix": "%(column_0_label)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_%(referred_table_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}

metadata = MetaData(naming_convention=convention)


def generate_uuid() -> uuid.UUID:
    """Generate a new UUID v4 for primary key columns."""
    return uuid.uuid4()


class Base(DeclarativeBase):
    metadata = metadata

    # Make the base class abstract (no table)
    __abstract__ = True

    def __repr__(self) -> str:
        """Generate a readable representation of model instances.

        Returns:
            String representation with class name and primary key
        """
        # Get primary key column(s)
        pk_columns = [col.name for col in self.__table__.primary_key]
        pk_values = [
            f"{col}={getattr(self, col, None)!r}" for col in pk_columns
        ]

        return f"{self.__class__.__name__}({', '.join(pk_values)})"


class UUIDPrimaryKeyMixin:
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=generate_uuid,
        doc="Unique identifier (UUID v4)",
    )


class TimestampMixin:
    """Mixin for created_at and updated_at timestamp columns.

    Automatically manages:
    - created_at: Set once on insert (never changes)
    - updated_at: Set on insert, updated on every modification
    """

    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(UTC),
        nullable=False,
        index=True,
        doc="Timestamp when record was created (UTC)",
    )

    updated_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
        index=False,
        doc="Timestamp when record was last updated (UTC)",
    )


@declarative_mixin
class VersionMixin:
    """Use ONLY for financial/quota tables (token usage, billing).

    Most chat API tables should NOT use this mixin:
    - Conversations (single-user access)
    - Messages (immutable)
    - Users (low conflict)
    - API Keys (use Redis for rate limiting)

    Use ONLY for:
    - UserQuota (prevent token quota bypass)
    - Subscription (prevent double-billing)
    - Credits/Wallet (if you have a credit system)
    """

    __mapper_args__ = {"version_id_col": "version"}

    version: Mapped[int] = mapped_column(
        default=1,
        nullable=False,
        doc="Version counter for optimistic locking (auto-managed by SQLAlchemy)",
    )
