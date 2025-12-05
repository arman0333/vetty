"""Tests for CoinGecko service."""

import pytest
from unittest.mock import AsyncMock, patch
from app.services.coingecko import CoinGeckoService
import httpx


@pytest.fixture
def coingecko_service():
    """Create a CoinGecko service instance."""
    return CoinGeckoService()


@pytest.mark.asyncio
async def test_get_all_coins(coingecko_service):
    """Test getting all coins."""
    mock_response = [
        {"id": "bitcoin", "symbol": "btc", "name": "Bitcoin"},
        {"id": "ethereum", "symbol": "eth", "name": "Ethereum"},
    ]

    async def mock_get(*args, **kwargs):
        mock_response_obj = AsyncMock()
        mock_response_obj.json = AsyncMock(return_value=mock_response)
        mock_response_obj.raise_for_status = AsyncMock()
        return mock_response_obj

    with patch.object(coingecko_service.client, "get", side_effect=mock_get):
        result = await coingecko_service.get_all_coins()
        assert len(result) == 2
        assert result[0]["id"] == "bitcoin"


@pytest.mark.asyncio
async def test_get_categories(coingecko_service):
    """Test getting categories."""
    mock_response = [
        {"category_id": "defi", "name": "DeFi"},
        {"category_id": "nft", "name": "NFT"},
    ]

    async def mock_get(*args, **kwargs):
        mock_response_obj = AsyncMock()
        mock_response_obj.json = AsyncMock(return_value=mock_response)
        mock_response_obj.raise_for_status = AsyncMock()
        return mock_response_obj

    with patch.object(coingecko_service.client, "get", side_effect=mock_get):
        result = await coingecko_service.get_categories()
        assert len(result) == 2
        assert result[0]["category_id"] == "defi"


@pytest.mark.asyncio
async def test_get_coin_market_data(coingecko_service):
    """Test getting coin market data."""
    mock_response_inr = [
        {
            "id": "bitcoin",
            "symbol": "btc",
            "name": "Bitcoin",
            "current_price": 5000000.0,
            "market_cap": 1000000000000,
        }
    ]

    mock_response_cad = [
        {
            "id": "bitcoin",
            "symbol": "btc",
            "name": "Bitcoin",
            "current_price": 85000.0,
            "market_cap": 1700000000000,
        }
    ]

    call_count = 0

    async def mock_get(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        mock_response_obj = AsyncMock()
        if kwargs.get("params", {}).get("vs_currency") == "cad":
            mock_response_obj.json.return_value = mock_response_cad
        else:
            mock_response_obj.json.return_value = mock_response_inr
        mock_response_obj.raise_for_status = AsyncMock()
        return mock_response_obj

    with patch.object(coingecko_service.client, "get", side_effect=mock_get):
        result = await coingecko_service.get_coin_market_data(
            coin_ids=["bitcoin"], vs_currencies=["inr", "cad"]
        )
        assert len(result) == 1
        assert result[0]["id"] == "bitcoin"
        assert "current_price_cad" in result[0]
        assert "market_cap_cad" in result[0]

