"""Utility functions shared across the application."""

import math
from typing import List, Any, Dict
from app.models import PaginatedResponse


def paginate_data(
    data: List[Any], page: int, per_page: int
) -> PaginatedResponse:
    """
    Paginate a list of data.

    Args:
        data: List of data to paginate
        page: Page number (1-indexed)
        per_page: Items per page

    Returns:
        PaginatedResponse object
    """
    total = len(data)
    total_pages = math.ceil(total / per_page) if total > 0 else 0
    start = (page - 1) * per_page
    end = start + per_page
    paginated_data = data[start:end]

    return PaginatedResponse(
        page=page,
        per_page=per_page,
        total=total,
        total_pages=total_pages,
        data=paginated_data,
    )


def format_market_data(coin: Dict[str, Any]) -> Dict[str, Any]:
    """
    Format coin market data for API response.

    Args:
        coin: Raw coin data from CoinGecko API

    Returns:
        Formatted coin data dictionary
    """
    return {
        "id": coin.get("id"),
        "symbol": coin.get("symbol"),
        "name": coin.get("name"),
        "current_price_inr": coin.get("current_price"),
        "current_price_cad": coin.get("current_price_cad"),
        "market_cap_inr": coin.get("market_cap"),
        "market_cap_cad": coin.get("market_cap_cad"),
        "price_change_percentage_24h": coin.get("price_change_percentage_24h"),
    }

