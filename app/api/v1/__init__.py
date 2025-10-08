from fastapi import APIRouter

from app.api.v1.examples import router as examples_router
from app.api.v1.users import router as users_router

router = APIRouter()

router.include_router(users_router, prefix="", tags=["v1"])
router.include_router(examples_router, prefix="", tags=["v1", "examples"])
