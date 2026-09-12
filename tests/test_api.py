"""
Unit tests for FastAPI REST endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_health_endpoint():
    """Verify health check endpoint returns 200 and healthy status."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "active_model" in data


def test_suggest_endpoint_mock():
    """Verify /v1/suggest endpoint processes requests successfully."""
    payload = {
        "subject": "Billing card update inquiry",
        "customer_email": "How can I update my expired card?",
        "mode": "zero_shot"
    }
    response = client.post("/v1/suggest", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "suggested_reply" in data
    assert len(data["suggested_reply"]) > 10
