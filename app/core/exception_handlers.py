"""
Exception handlers for FastAPI application.

Provides global exception handlers that:
- Log exceptions with full context
- Return consistent JSON error responses
- Handle environment-aware error details
"""

from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from loguru import logger
from sqlalchemy.exc import DatabaseError, SQLAlchemyError

from app.config import config
from app.schemas.error import ErrorDetail, ErrorResponse


async def handle_validation_error(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """
    Handle Pydantic validation errors.

    Args:
        request: The incoming request
        exc: The validation error exception

    Returns:
        JSONResponse with 422 status and validation error details
    """
    # Log validation error
    logger.warning(
        "Validation error on {method} {path}",
        method=request.method,
        path=request.url.path,
        errors=exc.errors(),
    )

    # Build error details - only include in development
    details = None
    if not config.is_production:
        details = {"validation_errors": exc.errors()}

    error_detail = ErrorDetail(
        type="validation_error",
        message="Invalid request data",
        details=details,
    )

    error_response = ErrorResponse(error=error_detail)

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=error_response.model_dump(),
    )


async def handle_database_error(
    request: Request, exc: SQLAlchemyError | DatabaseError
) -> JSONResponse:
    """
    Handle SQLAlchemy database errors.

    Args:
        request: The incoming request
        exc: The database error exception

    Returns:
        JSONResponse with 500 status and database error details
    """
    # Log database error with full context
    logger.error(
        "Database error on {method} {path}: {error}",
        method=request.method,
        path=request.url.path,
        error=str(exc),
        exc_info=True,
    )

    # Build error details - only include technical info in development
    details = None
    if not config.is_production:
        details = {"database_error": str(exc)}

    error_detail = ErrorDetail(
        type="database_error",
        message="A database error occurred",
        details=details,
    )

    error_response = ErrorResponse(error=error_detail)

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response.model_dump(),
    )


async def handle_generic_exception(
    request: Request, exc: Exception
) -> JSONResponse:
    """
    Handle all other unhandled exceptions.

    This is the catch-all handler for any exceptions not handled by
    more specific handlers.

    Args:
        request: The incoming request
        exc: The exception

    Returns:
        JSONResponse with 500 status and generic error message
    """
    # Log the exception with full traceback
    logger.exception(
        "Unhandled exception on {method} {path}: {error}",
        method=request.method,
        path=request.url.path,
        error=str(exc),
    )

    # Build error details - only include technical info in development
    details = None
    if not config.is_production:
        details = {
            "exception_type": type(exc).__name__,
            "exception_message": str(exc),
        }

    error_detail = ErrorDetail(
        type="internal_error",
        message="An internal error occurred",
        details=details,
    )

    error_response = ErrorResponse(error=error_detail)

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response.model_dump(),
    )
