"""FastAPI application entry point."""

from contextlib import asynccontextmanager
from typing import List

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from sqlalchemy.exc import DatabaseError, SQLAlchemyError

from app.api import router as default_router
from app.api.v1 import router as v1_router
from app.config import config
from app.core.exception_handlers import (
    handle_database_error,
    handle_generic_exception,
    handle_validation_error,
)
from app.core.logging import configure_logging
from app.db.engine import dispose_db, init_db


@asynccontextmanager
async def create_lifespan(app: FastAPI):
    # Startup: Initialize database engine and session factory
    logger.info(
        "Starting Project API v{version} on {env}",
        version=config.APP_VERSION,
        env=config.ENVIRONMENT.value,
    )
    await init_db()
    yield
    # Shutdown: Dispose database engine and close connections
    logger.info("Shutting down Project API")
    await dispose_db()


def create_middlewares() -> List[Middleware]:
    """Important: middleware order matters!"""
    return [
        Middleware(
            CORSMiddleware,
            allow_origins=config.ALLOWED_ORIGINS,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    ]


def register_routers(app_: FastAPI):
    app_.include_router(default_router)
    app_.include_router(v1_router, prefix="/api/v1")


def register_exception_handlers(app_: FastAPI):
    app_.add_exception_handler(RequestValidationError, handle_validation_error)
    app_.add_exception_handler(SQLAlchemyError, handle_database_error)
    app_.add_exception_handler(DatabaseError, handle_database_error)
    app_.add_exception_handler(Exception, handle_generic_exception)


def create_app() -> FastAPI:
    _app = FastAPI(
        title="Project API",
        version=config.APP_VERSION,
        description="API Endpoint for Project",
        docs_url=None if config.is_production else "/docs",
        redoc_url=None if config.is_production else "/redoc",
        swagger_ui_parameters={
            "tryItOutEnabled": True,
            "syntaxHighlight": {"theme": "nord"},
        },
        lifespan=create_lifespan,
        middleware=create_middlewares(),
    )
    register_routers(_app)
    register_exception_handlers(_app)
    return _app


# Configure logging before anything else
configure_logging()

app: FastAPI = create_app()
