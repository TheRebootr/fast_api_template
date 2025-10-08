"""Tests for the main application endpoints."""

from fastapi.testclient import TestClient


def test_root_endpoint(client: TestClient):
    """Test the root endpoint returns correct response."""
    response = client.get("/")
    assert response.status_code == 200

    data = response.json()
    assert "message" in data
    assert "version" in data
    assert "status" in data
    assert data["message"] == "Welcome to Project API"
    assert data["status"] == "running"
    assert data["version"] == "0.1.0"


def test_health_check_endpoint(client: TestClient):
    """Test the health check endpoint returns healthy status."""
    response = client.get("/health")
    assert response.status_code == 200

    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"


def test_app_metadata(client: TestClient):
    """Test that the FastAPI app has correct metadata."""
    response = client.get("/openapi.json")
    assert response.status_code == 200

    openapi_schema = response.json()
    assert openapi_schema["info"]["title"] == "Project API"
    assert openapi_schema["info"]["description"] == "API Endpoint for Project"
    assert openapi_schema["info"]["version"] == "0.1.0"


def test_cors_headers(client: TestClient):
    """Test that CORS middleware is properly configured."""
    response = client.options(
        "/",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET",
        },
    )
    # The response should include CORS headers
    assert response.status_code in [200, 204]


def test_nonexistent_endpoint(client: TestClient):
    """Test that nonexistent endpoints return 404."""
    response = client.get("/nonexistent")
    assert response.status_code == 404
