"""Shared test fixtures and configuration."""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI application."""
    return TestClient(app)


@pytest.fixture
def test_config():
    """Provide test configuration values."""
    return {
        "ENVIRONMENT": "test",
        "DEBUG": True,
        "APP_VERSION": "0.1.0",
        "ALLOWED_ORIGINS": [""],
    }
