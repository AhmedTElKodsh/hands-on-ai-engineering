"""
Test configuration.
"""

import pytest


@pytest.fixture
def test_client():
    """Create test client for API testing."""
    from fastapi.testclient import TestClient
    from app.main import app

    with TestClient(app) as client:
        yield client
