"""User endpoints (simple list)."""

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import CommonQueryParams, get_db
from app.models.user import User
from app.schemas.user import UserResponse

router = APIRouter()


@router.get("/users")
async def get_all_users(
    db: Annotated[AsyncSession, Depends(get_db)],
    pagination: Annotated[CommonQueryParams, Depends()],
) -> list[UserResponse]:
    """Return all users with pagination support.

    Args:
        db: Database session (injected)
        pagination: Pagination parameters (injected)

    Returns:
        List of users respecting pagination limits

    Note:
        Uses pagination parameters (skip/limit) to control result size.
        Default limit is 20, maximum is 100.
    """
    query = (
        select(User)
        .order_by(User.created_at)
        .offset(pagination.skip)
        .limit(pagination.limit)
    )
    result = await db.execute(query)
    users = result.scalars().all()
    return [UserResponse.model_validate(u) for u in users]
