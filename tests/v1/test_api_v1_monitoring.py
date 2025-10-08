"""Tests for the API v1 monitoring endpoints."""

from fastapi.testclient import TestClient


def test_v1_health_check_endpoint(client: TestClient):
    """Test the v1 health check endpoint returns correct response."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200

    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"

    # Check for service status indicators
    assert "postgres" in data
    assert "cache" in data
    assert data["cache"] == "connected"


def test_v1_health_check_returns_json(client: TestClient):
    """Test that the v1 health check endpoint returns JSON."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
