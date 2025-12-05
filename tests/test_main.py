"""Tests for main application."""

import pytest
from fastapi import status


def test_root_endpoint(client):
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert data["version"] == "1.0.0"


def test_health_check(client):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "healthy"


def test_docs_endpoint(client):
    """Test Swagger docs endpoint."""
    response = client.get("/docs")
    assert response.status_code == status.HTTP_200_OK


def test_redoc_endpoint(client):
    """Test ReDoc endpoint."""
    response = client.get("/redoc")
    assert response.status_code == status.HTTP_200_OK

