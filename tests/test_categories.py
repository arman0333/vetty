"""Tests for categories endpoints."""

import pytest
from fastapi import status
from unittest.mock import patch, MagicMock
import httpx


def test_list_categories_success(authenticated_client, mock_coingecko_response):
    """Test successful listing of categories."""
    with patch(
        "app.services.coingecko.coingecko_service.get_categories"
    ) as mock_get:
        mock_get.return_value = mock_coingecko_response["categories_list"]
        response = authenticated_client.get("/categories?page_num=1&per_page=10")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "page" in data
        assert "per_page" in data
        assert "total" in data
        assert "total_pages" in data
        assert "data" in data
        assert len(data["data"]) == 2


def test_list_categories_pagination(authenticated_client):
    """Test pagination for categories listing."""
    categories = [
        {"category_id": f"cat{i}", "name": f"Category {i}"} for i in range(15)
    ]
    with patch(
        "app.services.coingecko.coingecko_service.get_categories"
    ) as mock_get:
        mock_get.return_value = categories
        response = authenticated_client.get("/categories?page_num=1&per_page=5")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["page"] == 1
        assert data["per_page"] == 5
        assert data["total"] == 15
        assert data["total_pages"] == 3
        assert len(data["data"]) == 5


def test_get_category_coins_success(authenticated_client, mock_coingecko_response):
    """Test getting coins in a category."""
    from unittest.mock import AsyncMock
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
            "/categories/defi/coins?page_num=1&per_page=10"
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "data" in data
        assert len(data["data"]) > 0
        coin = data["data"][0]
        assert "current_price_inr" in coin
        assert "current_price_cad" in coin


def test_get_category_coins_invalid_category(authenticated_client):
    """Test getting coins for invalid category."""
    from unittest.mock import AsyncMock, MagicMock
    import httpx
    
    error = httpx.HTTPStatusError(
        "Not found", request=MagicMock(), response=MagicMock(status_code=404)
    )
    mock_get = AsyncMock(side_effect=error)
    with patch(
        "app.services.coingecko.coingecko_service.get_coin_market_data",
        side_effect=mock_get,
    ):
        response = authenticated_client.get(
            "/categories/invalid/coins?page_num=1&per_page=10"
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND


def test_list_categories_api_error(authenticated_client):
    """Test handling of API errors."""
    with patch(
        "app.services.coingecko.coingecko_service.get_categories"
    ) as mock_get:
        mock_get.side_effect = Exception("API Error")
        response = authenticated_client.get("/categories?page_num=1&per_page=10")
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR


def test_get_category_coins_api_error(authenticated_client):
    """Test handling of API errors for category coins."""
    from unittest.mock import AsyncMock
    
    mock_get = AsyncMock(side_effect=Exception("API Error"))
    with patch(
        "app.services.coingecko.coingecko_service.get_coin_market_data",
        side_effect=mock_get,
    ):
        response = authenticated_client.get(
            "/categories/defi/coins?page_num=1&per_page=10"
        )
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

