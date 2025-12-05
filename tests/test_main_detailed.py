"""Tests for main application detailed endpoints."""

import pytest
from unittest.mock import AsyncMock, patch
from fastapi import status
import httpx


def test_detailed_health_check_success(client):
    """Test detailed health check with successful CoinGecko API."""
    with patch("httpx.AsyncClient.get") as mock_get:
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.elapsed.total_seconds.return_value = 0.25
        mock_get.return_value = mock_response
        
        response = client.get("/health/detailed")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "healthy"
        assert "checks" in data
        assert data["checks"]["coingecko_api"]["status"] == "healthy"


def test_detailed_health_check_timeout(client):
    """Test detailed health check with CoinGecko API timeout."""
    with patch("httpx.AsyncClient.get", side_effect=httpx.TimeoutException("Timeout")):
        response = client.get("/health/detailed")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "degraded"
        assert data["checks"]["coingecko_api"]["status"] == "unhealthy"


def test_version_info(client):
    """Test version information endpoint."""
    response = client.get("/version")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "application" in data
    assert "dependencies" in data
    assert "external_services" in data
    assert data["application"]["version"] == "1.0.0"
    assert "fastapi" in data["dependencies"]


def test_version_info_coingecko_status(client):
    """Test version info includes CoinGecko status."""
    async def mock_get(*args, **kwargs):
        mock_response = AsyncMock()
        mock_response.status_code = 200
        return mock_response
    
    with patch("httpx.AsyncClient.get", side_effect=mock_get):
        response = client.get("/version")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["external_services"]["coingecko"]["status"] == "available"

