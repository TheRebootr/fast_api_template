"""Pydantic schemas for User model API validation and serialization."""

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class UserBase(BaseModel):
    """Base schema with common User fields.

    Currently minimal - only contains ID.
    Future fields (email, name, etc.) can be added here.
    """

    pass  # No editable fields in basic User model


class UserCreate(UserBase):
    """Schema for creating a new user.

    Request body for POST /users endpoint.
    Currently no required fields (ID is auto-generated).
    """

    id: uuid.UUID | None = Field(
        default=None,
        description="Optional explicit UUID (auto-generated if omitted)",
    )


class UserUpdate(UserBase):
    """Schema for updating an existing user.

    Request body for PATCH /users/{id} endpoint.
    Currently no editable fields in basic User model.
    Future: Add optional fields that can be updated.
    """

    pass


class UserResponse(UserBase):
    """Schema for User API responses.

    Returned from all User endpoints (GET, POST, PATCH).

    Fields:
    - id: UUID of user
    - name: Optional user name
    - created_at: Creation timestamp (ISO 8601)
    - updated_at: Last update timestamp (ISO 8601)
    - version: Optimistic locking version
    """

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID = Field(description="Unique user identifier (UUID)")
    name: str | None = Field(default=None, description="Optional user name")
    created_at: datetime = Field(
        description="Creation timestamp (UTC, ISO 8601)"
    )
    updated_at: datetime = Field(
        description="Last update timestamp (UTC, ISO 8601)"
    )
    version: int = Field(description="Version number for optimistic locking")


class UserListResponse(BaseModel):
    """Schema for paginated list of users.

    Returned from GET /users endpoint.

    Fields:
    - items: List of User objects
    - total: Total count of users (for pagination)
    - offset: Current offset
    - limit: Current page size
    """

    items: list[UserResponse] = Field(description="List of users")
    total: int = Field(description="Total number of users")
    offset: int = Field(default=0, description="Pagination offset")
    limit: int = Field(default=100, description="Pagination limit")
