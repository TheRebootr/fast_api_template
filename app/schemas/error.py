"""Error response schemas for consistent API error handling."""

from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class ErrorDetail(BaseModel):
    """Detailed error information.

    Attributes:
        type: Error type identifier (e.g., "validation_error",
            "database_error")
        message: Human-readable error message safe to display to clients
        details: Additional context, only included in development
            environment
    """

    type: str = Field(..., description="Error type identifier")
    message: str = Field(..., description="Human-readable error message")
    details: Optional[Dict[str, Any]] = Field(
        None, description="Additional context (development only)"
    )


class ErrorResponse(BaseModel):
    """Top-level error response wrapper.

    Attributes:
        error: The error details
    """

    error: ErrorDetail = Field(..., description="Error details")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "error": {
                        "type": "validation_error",
                        "message": "Invalid input data",
                        "details": {
                            "field": "email",
                            "issue": "Invalid format",
                        },
                    }
                }
            ]
        }
    }
