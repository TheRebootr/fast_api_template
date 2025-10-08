"""Database session dependency for FastAPI.

IMPORTANT:
    Avoid ``from app.db.engine import AsyncSessionLocal`` because that copies
    a possibly ``None`` value at import time. After ``init_db()`` runs it
    assigns a new factory to ``engine.AsyncSessionLocal``, but this module
    would still hold the old ``None`` reference and raise the runtime error
    about initialization. Import the engine module and read the attribute
    dynamically instead.
"""

from collections.abc import AsyncGenerator
from typing import cast

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.db import engine as db_engine


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency that provides database sessions.

    Lifecycle:
    1. Create new AsyncSession from factory
    2. Yield session to request handler
    3. Close session (return connection to pool)

    Transaction Management:
    - Use db.flush() to get generated IDs without committing
    - Manual commits create checkpoints that won't rollback

    Usage in FastAPI routes:
        @app.get("/users/{user_id}")
        async def get_user(
            user_id: str,
            db: AsyncSession = Depends(get_db)
        ):
            return await db.get(User, user_id)

        @app.post("/users")
        async def create_user(
            name: str,
            db: AsyncSession = Depends(get_db)
        ):
            try:
                user = User(name=name)
                db.add(user)
                db.flush()  # Get user.id without committing
                db.commit()  # Commit transaction
                return {"id": user.id}
            except IntegrityError as e:
                db.rollback()
                logger.error(f"Error: {e}")
                raise HTTPException(400, "User exists")

    Yields:
        AsyncSession instance for database operations

    Raises:
        RuntimeError: If called before database initialization
    """
    # Access the session factory dynamically from the engine module to avoid
    # stale references caused by direct symbol import at module import time.
    # May be None until init_db() runs in the app lifespan.
    session_factory = db_engine.AsyncSessionLocal

    if session_factory is None:
        raise RuntimeError(
            "Database not initialized. "
            "Call init_db() during application startup."
        )

    async with cast(async_sessionmaker, session_factory)() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            # Always close session (return connection to pool)
            await session.close()
