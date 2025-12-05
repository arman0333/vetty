"""Coins router."""

from fastapi import APIRouter, Query, Depends, HTTPException, status
from typing import Optional
import httpx
from app.models import PaginatedResponse
from app.services.coingecko import coingecko_service
from app.auth import get_current_user
from app.config import settings
from app.utils import paginate_data, format_market_data

router = APIRouter(prefix="/coins", tags=["coins"])


@router.get("", response_model=PaginatedResponse)
async def list_coins(
    page_num: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(
        None, ge=1, le=250, description="Items per page"
    ),
    current_user: dict = Depends(get_current_user),
):
    """
    List all coins with pagination.

    Args:
        page_num: Page number (default: 1)
        per_page: Items per page (default: 10)
        current_user: Current authenticated user

    Returns:
        Paginated list of coins with id, symbol, and name
    """
    if per_page is None:
        per_page = settings.default_per_page

    try:
        coins = await coingecko_service.get_all_coins()
        return paginate_data(coins, page_num, per_page)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching coins: {str(e)}",
        )


@router.get("/market-data", response_model=PaginatedResponse)
async def get_coin_market_data(
    coin_id: Optional[str] = Query(
        None, description="Coin ID(s) from /coins endpoint (comma-separated: bitcoin,ethereum)"
    ),
    category: Optional[str] = Query(
        None, description="Category ID from /categories endpoint"
    ),
    page_num: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(
        None, ge=1, le=250, description="Items per page"
    ),
    current_user: dict = Depends(get_current_user),
):
    """
    List specific coins according to id from listing endpoint and/or category 
    from categories endpoint. Shows market data in INR and CAD.
    
    This endpoint allows filtering coins by:
    - coin_id: One or more coin IDs from the /coins listing endpoint
    - category: A category ID from the /categories endpoint
    - Both: Use coin_id AND category together for combined filtering

    Args:
        coin_id: Optional coin ID(s) from /coins endpoint (comma-separated for multiple)
        category: Optional category ID from /categories endpoint
        page_num: Page number (default: 1)
        per_page: Items per page (default: 10)
        current_user: Current authenticated user

    Returns:
        Paginated list of coins with market data in INR and CAD
        
    Examples:
        - Get coins by ID: /coins/market-data?coin_id=bitcoin,ethereum
        - Get coins by category: /coins/market-data?category=defi
        - Get coins by both: /coins/market-data?coin_id=bitcoin&category=defi
    """
    if per_page is None:
        per_page = settings.default_per_page

    # Validate that at least one filter is provided
    if not coin_id and not category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one of 'coin_id' or 'category' must be provided",
        )

    # Parse comma-separated coin IDs
    coin_ids = None
    if coin_id:
        coin_ids = [cid.strip() for cid in coin_id.split(",") if cid.strip()]
        if not coin_ids:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid coin_id format",
            )

    try:
        market_data = await coingecko_service.get_coin_market_data(
            coin_ids=coin_ids,
            category=category,
            vs_currencies=["inr", "cad"],
        )

        formatted_data = [format_market_data(coin) for coin in market_data]
        return paginate_data(formatted_data, page_num, per_page)
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Coin or category not found",
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching coin data: {str(e)}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching coin data: {str(e)}",
        )


@router.get("/{coin_id}", response_model=PaginatedResponse)
async def get_coin_by_id(
    coin_id: str,
    page_num: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(
        None, ge=1, le=250, description="Items per page"
    ),
    category: Optional[str] = Query(None, description="Filter by category"),
    current_user: dict = Depends(get_current_user),
):
    """
    Get specific coin details by ID with market data in INR and CAD.
    
    Alternative endpoint that accepts coin_id as path parameter.
    Can also filter by category.

    Args:
        coin_id: Coin ID (use comma-separated for multiple: 'bitcoin,ethereum')
        page_num: Page number (default: 1)
        per_page: Items per page (default: 10)
        category: Optional category ID to filter coins
        current_user: Current authenticated user

    Returns:
        Paginated list of coins with market data in INR and CAD
    """
    if per_page is None:
        per_page = settings.default_per_page

    # Parse comma-separated coin IDs
    coin_ids = [cid.strip() for cid in coin_id.split(",") if cid.strip()]

    try:
        market_data = await coingecko_service.get_coin_market_data(
            coin_ids=coin_ids if coin_ids else None,
            category=category,
            vs_currencies=["inr", "cad"],
        )

        formatted_data = [format_market_data(coin) for coin in market_data]
        return paginate_data(formatted_data, page_num, per_page)
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Coin or category not found",
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching coin data: {str(e)}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching coin data: {str(e)}",
        )

