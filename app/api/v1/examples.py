"""Example endpoints demonstrating dependency injection patterns.

This module showcases various FastAPI dependency injection patterns
used throughout the Project API project.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import (
    CommonQueryParams,
    SearchQueryParams,
    get_db,
    get_settings,
)
from app.config import Settings
from app.models.user import User
from app.schemas.user import UserResponse

router = APIRouter()


@router.get("/examples/users/paginated")
async def get_paginated_users(
    db: Annotated[AsyncSession, Depends(get_db)],
    pagination: Annotated[CommonQueryParams, Depends()],
) -> dict:
    """Example: Basic pagination using CommonQueryParams.

    Query parameters:
        - skip: Number of records to skip (default: 0)
        - limit: Max records to return (default: 20, max: 100)

    Example:
        GET /api/v1/examples/users/paginated?skip=0&limit=10
    """
    # Get total count
    count_query = select(func.count()).select_from(User)
    total = await db.scalar(count_query) or 0

    # Get paginated results
    query = (
        select(User)
        .order_by(User.created_at.desc())
        .offset(pagination.skip)
        .limit(pagination.limit)
    )
    result = await db.execute(query)
    users = result.scalars().all()

    return {
        "total": total,
        "skip": pagination.skip,
        "limit": pagination.limit,
        "users": [UserResponse.model_validate(u) for u in users],
    }


@router.get("/examples/users/search")
async def search_users(
    db: Annotated[AsyncSession, Depends(get_db)],
    search: Annotated[SearchQueryParams, Depends()],
    pagination: Annotated[CommonQueryParams, Depends()],
) -> dict:
    """Example: Search with pagination and sorting.

    Query parameters:
        - q: Search query (searches in name and title)
        - sort_by: Field to sort by (name, title, created_at)
        - order: Sort order (asc or desc)
        - skip: Number of records to skip
        - limit: Max records to return

    Example:
        GET /api/v1/examples/users/search?q=john&sort_by=name&order=desc
    """
    query = select(User)

    # Apply search filter
    if search.q:
        search_term = f"%{search.q}%"
        query = query.where(
            (User.name.ilike(search_term)) | (User.title.ilike(search_term))
        )

    # Apply sorting
    if search.sort_by:
        sort_column = getattr(User, search.sort_by, None)
        if sort_column is None:
            raise HTTPException(
                400,
                f"Invalid sort_by field: {search.sort_by}",
            )

        if search.order == "desc":
            query = query.order_by(sort_column.desc())
        else:
            query = query.order_by(sort_column)
    else:
        # Default sorting
        query = query.order_by(User.created_at.desc())

    # Get total count (before pagination)
    count_query = select(func.count()).select_from(query.subquery())
    total = await db.scalar(count_query) or 0

    # Apply pagination
    query = query.offset(pagination.skip).limit(pagination.limit)

    # Execute query
    result = await db.execute(query)
    users = result.scalars().all()

    return {
        "total": total,
        "skip": pagination.skip,
        "limit": pagination.limit,
        "query": search.q,
        "sort_by": search.sort_by,
        "order": search.order,
        "users": [UserResponse.model_validate(u) for u in users],
    }


@router.get("/examples/info")
async def get_api_info(
    settings: Annotated[Settings, Depends(get_settings)],
) -> dict:
    """Example: Access application settings via dependency injection.

    Returns:
        Application configuration and metadata
    """
    return {
        "app": "Project API",
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT.value,
        "debug_mode": settings.DEBUG,
        "database_provider": settings.POSTGRES_PROVIDER.value,
    }


@router.get("/examples/multi-dependency")
async def multi_dependency_example(
    db: Annotated[AsyncSession, Depends(get_db)],
    settings: Annotated[Settings, Depends(get_settings)],
    pagination: Annotated[CommonQueryParams, Depends()],
) -> dict:
    """Example: Multiple dependencies in single endpoint.

    Demonstrates how to combine:
    - Database session
    - Application settings
    - Query parameters

    This pattern is useful for complex endpoints that need
    multiple injected dependencies.
    """
    # Use database
    count_query = select(func.count()).select_from(User)
    total_users = await db.scalar(count_query) or 0

    # Use settings
    env_info = {
        "environment": settings.ENVIRONMENT.value,
        "version": settings.APP_VERSION,
    }

    # Use pagination
    pagination_info = {
        "skip": pagination.skip,
        "limit": pagination.limit,
    }

    return {
        "environment": env_info,
        "pagination": pagination_info,
        "total_users": total_users,
        "message": "This endpoint demonstrates multiple dependencies",
    }
