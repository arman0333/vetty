"""Categories router."""

from fastapi import APIRouter, Query, Depends, HTTPException, status
from typing import Optional
import httpx
from app.models import PaginatedResponse
from app.services.coingecko import coingecko_service
from app.auth import get_current_user
from app.config import settings
from app.utils import paginate_data, format_market_data

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("", response_model=PaginatedResponse)
async def list_categories(
    page_num: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(
        None, ge=1, le=250, description="Items per page"
    ),
    current_user: dict = Depends(get_current_user),
):
    """
    List all coin categories with pagination.

    Args:
        page_num: Page number (default: 1)
        per_page: Items per page (default: 10)
        current_user: Current authenticated user

    Returns:
        Paginated list of categories
    """
    if per_page is None:
        per_page = settings.default_per_page

    try:
        categories = await coingecko_service.get_categories()
        # Format categories to match expected structure
        formatted_categories = []
        for cat in categories:
            formatted_categories.append(
                {
                    "category_id": cat.get("category_id", ""),
                    "name": cat.get("name", ""),
                }
            )
        return paginate_data(formatted_categories, page_num, per_page)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching categories: {str(e)}",
        )


@router.get("/{category_id}/coins", response_model=PaginatedResponse)
async def get_category_coins(
    category_id: str,
    page_num: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(
        None, ge=1, le=250, description="Items per page"
    ),
    current_user: dict = Depends(get_current_user),
):
    """
    Get coins in a specific category with market data in INR and CAD.

    Args:
        category_id: Category ID
        page_num: Page number (default: 1)
        per_page: Items per page (default: 10)
        current_user: Current authenticated user

    Returns:
        Paginated list of coins in the category with market data in INR and CAD
    """
    if per_page is None:
        per_page = settings.default_per_page

    try:
        market_data = await coingecko_service.get_coin_market_data(
            coin_ids=None,
            category=category_id,
            vs_currencies=["inr", "cad"],
        )

        formatted_data = [format_market_data(coin) for coin in market_data]
        return paginate_data(formatted_data, page_num, per_page)
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found",
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching category coins: {str(e)}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching category coins: {str(e)}",
        )

