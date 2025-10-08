"""Import all models to ensure they're registered with Base.metadata."""

from app.models.user import User  # noqa: F401

__all__ = ["User"]
