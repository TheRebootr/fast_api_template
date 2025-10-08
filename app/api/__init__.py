from fastapi import APIRouter

from app.config import config

router = APIRouter()


@router.get("/")
async def root():
    return {
        "message": "Welcome to Project API",
        "version": config.APP_VERSION,
        "status": "running",
    }


@router.get("/health")
async def health_check():
    return {"status": "healthy"}
