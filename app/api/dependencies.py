"""Shared dependencies for FastAPI endpoints.

This module provides reusable dependency functions that can be injected
into route handlers using FastAPI's Depends() system.

Example usage:
    from app.api.dependencies import get_db, get_settings, CommonQueryParams

    @router.get("/users")
    async def list_users(
        db: Annotated[AsyncSession, Depends(get_db)],
        pagination: Annotated[CommonQueryParams, Depends()],
        settings: Annotated[Settings, Depends(get_settings)],
    ):
        ...
"""

from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings, config
from app.db.session import get_db_session

# ===========================================================================
# Database Dependencies
# ===========================================================================


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for database session injection.

    This is a convenience wrapper around get_db_session() to keep the
    dependency name short and consistent with FastAPI conventions.

    Yields:
        AsyncSession: Database session for the request lifecycle

    Example:
        @router.get("/users/{user_id}")
        async def get_user(
            user_id: int,
            db: Annotated[AsyncSession, Depends(get_db)],
        ):
            result = await db.execute(select(User).where(User.id == user_id))
            return result.scalar_one_or_none()
    """
    async for session in get_db_session():
        yield session


# ===========================================================================
# Configuration Dependencies
# ===========================================================================


def get_settings() -> Settings:
    """Dependency for application settings injection.

    Returns the global configuration object. Useful for accessing
    settings in route handlers without importing config directly.

    Returns:
        Settings: Application configuration

    Example:
        @router.get("/info")
        async def get_info(
            settings: Annotated[Settings, Depends(get_settings)],
        ):
            return {
                "version": settings.APP_VERSION,
                "environment": settings.ENVIRONMENT,
            }
    """
    return config


# ===========================================================================
# Common Query Parameters
# ===========================================================================


class CommonQueryParams:
    """Common query parameters for list endpoints with pagination.

    This class can be used as a dependency to provide consistent
    pagination parameters across multiple endpoints.

    Attributes:
        skip: Number of records to skip (offset)
        limit: Maximum number of records to return

    Example:
        @router.get("/users")
        async def list_users(
            params: Annotated[CommonQueryParams, Depends()],
            db: Annotated[AsyncSession, Depends(get_db)],
        ):
            query = select(User).offset(params.skip).limit(params.limit)
            result = await db.execute(query)
            return result.scalars().all()
    """

    def __init__(
        self,
        skip: Annotated[
            int, Query(ge=0, description="Number of records to skip")
        ] = 0,
        limit: Annotated[
            int,
            Query(
                ge=1,
                le=100,
                description="Maximum number of records to return",
            ),
        ] = 20,
    ):
        self.skip = skip
        self.limit = limit


class SearchQueryParams:
    """Common search query parameters for endpoints with search/filter.

    Attributes:
        q: Search query string
        sort_by: Field to sort by
        order: Sort order (asc or desc)

    Example:
        @router.get("/users/search")
        async def search_users(
            search: Annotated[SearchQueryParams, Depends()],
            db: Annotated[AsyncSession, Depends(get_db)],
        ):
            query = select(User)
            if search.q:
                query = query.where(User.name.ilike(f"%{search.q}%"))
            return await db.execute(query)
    """

    def __init__(
        self,
        q: Annotated[str | None, Query(description="Search query")] = None,
        sort_by: Annotated[
            str | None,
            Query(description="Field to sort by"),
        ] = None,
        order: Annotated[
            str,
            Query(pattern="^(asc|desc)$", description="Sort order"),
        ] = "asc",
    ):
        self.q = q
        self.sort_by = sort_by
        self.order = order


# ===========================================================================
# Authentication Dependencies (Stubs for future implementation)
# ===========================================================================


async def get_current_user():
    """Dependency for current authenticated user.

    TODO: Implement actual authentication logic
    - Validate JWT token from Authorization header
    - Extract user claims
    - Load user from database
    - Handle token expiration

    Returns:
        User: Currently authenticated user

    Raises:
        HTTPException: 401 if authentication fails

    Example:
        @router.get("/me")
        async def get_current_user_info(
            current_user: Annotated[User, Depends(get_current_user)],
        ):
            return current_user
    """
    # Placeholder implementation
    # In production, this should:
    # 1. Extract and validate JWT token
    # 2. Query user from database
    # 3. Raise HTTPException(401) if invalid
    raise NotImplementedError("Authentication not yet implemented")


async def require_admin():
    """Dependency for admin-only endpoints.

    TODO: Implement role-based access control
    - Check if current user has admin role
    - Validate permissions

    Returns:
        User: Current user (if admin)

    Raises:
        HTTPException: 403 if user is not an admin

    Example:
        @router.delete("/users/{user_id}")
        async def delete_user(
            user_id: int,
            admin: Annotated[User, Depends(require_admin)],
            db: Annotated[AsyncSession, Depends(get_db)],
        ):
            # Only admins can access this endpoint
            ...
    """
    # Placeholder implementation
    raise NotImplementedError("Authorization not yet implemented")


# ===========================================================================
# Health Check Dependencies
# ===========================================================================


async def get_db_health() -> dict[str, bool]:
    """Dependency for database health check status.

    Returns:
        dict: Database health status

    Example:
        @router.get("/health")
        async def health_check(
            db_status: Annotated[dict, Depends(get_db_health)],
        ):
            return {"database": db_status}
    """
    from app.db.engine import check_db_health

    return {"status": await check_db_health()}
