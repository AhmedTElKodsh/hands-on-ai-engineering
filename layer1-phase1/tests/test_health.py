"""
Tests for health check endpoints.
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check():
    """Test health check endpoint returns healthy status."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "app" in data
    assert "environment" in data


def test_version_endpoint():
    """Test version endpoint returns version information."""
    response = client.get("/version")
    assert response.status_code == 200
    data = response.json()
    assert "version" in data
    assert "app" in data
    assert data["version"] == "0.1.0"


def test_request_id_header():
    """Test that responses include X-Request-ID header."""
    response = client.get("/health")
    assert response.status_code == 200
    assert "X-Request-ID" in response.headers
    # Verify it's a valid UUID
    import uuid
    try:
        uuid.UUID(response.headers["X-Request-ID"])
    except ValueError:
        pytest.fail("X-Request-ID is not a valid UUID")
