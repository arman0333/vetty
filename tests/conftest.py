"""Pytest configuration and fixtures."""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, MagicMock, patch
from app.main import app
from app.auth import create_access_token
from app.config import settings
from datetime import timedelta


@pytest.fixture
def client():
    """Create a test client."""
    return TestClient(app)


@pytest.fixture
def auth_token():
    """Create a test JWT token."""
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    token = create_access_token(
        data={"sub": "testuser"}, expires_delta=access_token_expires
    )
    return token


@pytest.fixture
def authenticated_client(client, auth_token):
    """Create an authenticated test client."""
    client.headers.update({"Authorization": f"Bearer {auth_token}"})
    return client


@pytest.fixture
def mock_coingecko_response():
    """Mock CoinGecko API responses."""
    return {
        "coins_list": [
            {"id": "bitcoin", "symbol": "btc", "name": "Bitcoin"},
            {"id": "ethereum", "symbol": "eth", "name": "Ethereum"},
        ],
        "categories_list": [
            {"category_id": "defi", "name": "DeFi"},
            {"category_id": "nft", "name": "NFT"},
        ],
        "market_data": [
            {
                "id": "bitcoin",
                "symbol": "btc",
                "name": "Bitcoin",
                "current_price": 5000000.0,
                "market_cap": 1000000000000,
                "price_change_percentage_24h": 2.5,
            }
        ],
        "market_data_cad": [
            {
                "id": "bitcoin",
                "symbol": "btc",
                "name": "Bitcoin",
                "current_price": 85000.0,
                "market_cap": 1700000000000,
            }
        ],
    }

