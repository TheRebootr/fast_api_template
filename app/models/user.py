"""User database model with async SQLAlchemy 2.0."""

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin, VersionMixin


class User(Base, TimestampMixin, VersionMixin, UUIDPrimaryKeyMixin):
    """User entity representing a user account.

    Columns:
    - id: UUID primary key (auto-generated)
    - created_at: Timestamp when user was created (auto-generated, indexed)
    - updated_at: Timestamp when user was last updated
      (auto-updated, indexed)
    - version: Optimistic locking version counter
      (starts at 1, auto-incremented)

    Mixins:
    - TimestampMixin: Provides created_at and updated_at
    - VersionMixin: Provides version for optimistic locking
    - UUIDPrimaryKeyMixin: Provides UUID primary key id

    Example:
        # Create user with auto-generated ID
        user = User()
        session.add(user)
        await session.commit()

        # Create user with explicit ID
        user = User(id=uuid.uuid4())
        session.add(user)
        await session.commit()

        # Update user (version auto-increments)
        user.updated_at = datetime.now(UTC)  # Trigger update
        await session.commit()
        assert user.version == 2
    """

    __tablename__ = "users"

    name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        doc="Optional user name",
    )

    title: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        doc="Optional user title",
    )

    def __repr__(self) -> str:
        """Return string representation of User instance.

        Returns:
            String with class name and ID
        """
        return f"User(id={self.id!r})"
