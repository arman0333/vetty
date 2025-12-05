"""Tests for coins endpoints."""

import pytest
from fastapi import status
from unittest.mock import patch, AsyncMock, MagicMock


def test_list_coins_success(authenticated_client, mock_coingecko_response):
    """Test successful listing of coins."""
    with patch(
        "app.services.coingecko.coingecko_service.get_all_coins"
    ) as mock_get:
        mock_get.return_value = mock_coingecko_response["coins_list"]
        response = authenticated_client.get("/coins?page_num=1&per_page=10")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "page" in data
        assert "per_page" in data
        assert "total" in data
        assert "total_pages" in data
        assert "data" in data
        assert len(data["data"]) == 2


def test_list_coins_pagination(authenticated_client, mock_coingecko_response):
    """Test pagination for coins listing."""
    coins = [
        {"id": f"coin{i}", "symbol": f"c{i}", "name": f"Coin {i}"}
        for i in range(25)
    ]
    with patch(
        "app.services.coingecko.coingecko_service.get_all_coins"
    ) as mock_get:
        mock_get.return_value = coins
        response = authenticated_client.get("/coins?page_num=1&per_page=10")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["page"] == 1
        assert data["per_page"] == 10
        assert data["total"] == 25
        assert data["total_pages"] == 3
        assert len(data["data"]) == 10

        # Test second page
        response = authenticated_client.get("/coins?page_num=2&per_page=10")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["page"] == 2
        assert len(data["data"]) == 10


def test_list_coins_default_pagination(authenticated_client, mock_coingecko_response):
    """Test default pagination."""
    with patch(
        "app.services.coingecko.coingecko_service.get_all_coins"
    ) as mock_get:
        mock_get.return_value = mock_coingecko_response["coins_list"]
        response = authenticated_client.get("/coins?page_num=1")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["per_page"] == 10  # Default per_page


def test_get_coin_details_success(authenticated_client, mock_coingecko_response):
    """Test getting specific coin details."""
    market_data = mock_coingecko_response["market_data"]
    market_data_cad = mock_coingecko_response["market_data_cad"]
    
    # Merge CAD data into market data
    result = market_data.copy()
    result[0]["current_price_cad"] = market_data_cad[0]["current_price"]
    result[0]["market_cap_cad"] = market_data_cad[0]["market_cap"]

    mock_get = AsyncMock(return_value=result)
    with patch(
        "app.services.coingecko.coingecko_service.get_coin_market_data",
        side_effect=mock_get,
    ):
        response = authenticated_client.get("/coins/bitcoin?page_num=1&per_page=10")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "data" in data
        assert len(data["data"]) > 0
        coin = data["data"][0]
        assert "current_price_inr" in coin
        assert "current_price_cad" in coin
        assert "market_cap_inr" in coin
        assert "market_cap_cad" in coin


def test_get_coin_details_with_category(authenticated_client, mock_coingecko_response):
    """Test getting coin details filtered by category."""
    market_data = mock_coingecko_response["market_data"]
    market_data_cad = mock_coingecko_response["market_data_cad"]
    
    result = market_data.copy()
    result[0]["current_price_cad"] = market_data_cad[0]["current_price"]
    result[0]["market_cap_cad"] = market_data_cad[0]["market_cap"]

    mock_get = AsyncMock(return_value=result)
    with patch(
        "app.services.coingecko.coingecko_service.get_coin_market_data",
        side_effect=mock_get,
    ):
        response = authenticated_client.get(
            "/coins/bitcoin?category=defi&page_num=1&per_page=10"
        )
        assert response.status_code == status.HTTP_200_OK


def test_get_coin_details_multiple_ids(authenticated_client, mock_coingecko_response):
    """Test getting details for multiple coin IDs."""
    market_data = [
        {
            "id": "bitcoin",
            "symbol": "btc",
            "name": "Bitcoin",
            "current_price": 5000000.0,
            "market_cap": 1000000000000,
            "price_change_percentage_24h": 2.5,
            "current_price_cad": 85000.0,
            "market_cap_cad": 1700000000000,
        },
        {
            "id": "ethereum",
            "symbol": "eth",
            "name": "Ethereum",
            "current_price": 300000.0,
            "market_cap": 500000000000,
            "price_change_percentage_24h": 1.5,
            "current_price_cad": 5100.0,
            "market_cap_cad": 850000000000,
        },
    ]

    mock_get = AsyncMock(return_value=market_data)
    with patch(
        "app.services.coingecko.coingecko_service.get_coin_market_data",
        side_effect=mock_get,
    ):
        response = authenticated_client.get(
            "/coins/bitcoin,ethereum?page_num=1&per_page=10"
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["data"]) == 2


def test_get_coin_details_invalid_coin(authenticated_client):
    """Test getting details for invalid coin ID."""
    import httpx
    from unittest.mock import MagicMock

    error = httpx.HTTPStatusError(
        "Not found", request=MagicMock(), response=MagicMock(status_code=404)
    )
    mock_get = AsyncMock(side_effect=error)
    with patch(
        "app.services.coingecko.coingecko_service.get_coin_market_data",
        side_effect=mock_get,
    ):
        response = authenticated_client.get("/coins/invalidcoin?page_num=1&per_page=10")
        assert response.status_code == status.HTTP_404_NOT_FOUND


def test_list_coins_api_error(authenticated_client):
    """Test handling of API errors."""
    with patch(
        "app.services.coingecko.coingecko_service.get_all_coins"
    ) as mock_get:
        mock_get.side_effect = Exception("API Error")
        response = authenticated_client.get("/coins?page_num=1&per_page=10")
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR


def test_pagination_validation(authenticated_client, mock_coingecko_response):
    """Test pagination parameter validation."""
    with patch(
        "app.services.coingecko.coingecko_service.get_all_coins"
    ) as mock_get:
        mock_get.return_value = mock_coingecko_response["coins_list"]
        # Test invalid page_num
        response = authenticated_client.get("/coins?page_num=0&per_page=10")
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

        # Test invalid per_page
        response = authenticated_client.get("/coins?page_num=1&per_page=0")
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

