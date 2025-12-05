"""Tests for utility functions."""

import pytest
from app.utils import paginate_data, format_market_data


def test_paginate_data():
    """Test pagination function."""
    data = [{"id": i} for i in range(25)]
    result = paginate_data(data, page=1, per_page=10)
    
    assert result.page == 1
    assert result.per_page == 10
    assert result.total == 25
    assert result.total_pages == 3
    assert len(result.data) == 10
    
    # Test second page
    result = paginate_data(data, page=2, per_page=10)
    assert result.page == 2
    assert len(result.data) == 10
    
    # Test empty data
    result = paginate_data([], page=1, per_page=10)
    assert result.total == 0
    assert result.total_pages == 0


def test_format_market_data():
    """Test market data formatting."""
    coin = {
        "id": "bitcoin",
        "symbol": "btc",
        "name": "Bitcoin",
        "current_price": 50000.0,
        "current_price_cad": 85000.0,
        "market_cap": 1000000000,
        "market_cap_cad": 1700000000,
        "price_change_percentage_24h": 2.5,
    }
    
    result = format_market_data(coin)
    
    assert result["id"] == "bitcoin"
    assert result["symbol"] == "btc"
    assert result["name"] == "Bitcoin"
    assert result["current_price_inr"] == 50000.0
    assert result["current_price_cad"] == 85000.0
    assert result["market_cap_inr"] == 1000000000
    assert result["market_cap_cad"] == 1700000000
    assert result["price_change_percentage_24h"] == 2.5

