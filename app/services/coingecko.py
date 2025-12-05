"""CoinGecko API service."""

import httpx
from typing import List, Optional, Dict, Any
from app.config import settings


class CoinGeckoService:
    """Service for interacting with CoinGecko API."""

    def __init__(self):
        """Initialize the service with API URL."""
        self.base_url = settings.coingecko_api_url
        self.client = httpx.AsyncClient(timeout=30.0)

    async def get_all_coins(self) -> List[Dict[str, Any]]:
        """
        Fetch all coins from CoinGecko API.

        Returns:
            List of coin dictionaries with id, symbol, and name
        """
        url = f"{self.base_url}/coins/list"
        response = await self.client.get(url)
        response.raise_for_status()
        return response.json()

    async def get_categories(self) -> List[Dict[str, Any]]:
        """
        Fetch all coin categories from CoinGecko API.

        Returns:
            List of category dictionaries
        """
        url = f"{self.base_url}/coins/categories/list"
        response = await self.client.get(url)
        response.raise_for_status()
        return response.json()

    async def get_coin_market_data(
        self,
        coin_ids: Optional[List[str]] = None,
        category: Optional[str] = None,
        vs_currencies: List[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Fetch market data for specific coins.

        Args:
            coin_ids: List of coin IDs to fetch
            category: Category ID to filter coins
            vs_currencies: List of currencies (default: ['inr', 'cad'])

        Returns:
            List of coin market data dictionaries
        """
        if vs_currencies is None:
            vs_currencies = ["inr", "cad"]

        url = f"{self.base_url}/coins/markets"
        params = {
            "vs_currency": vs_currencies[0],
            "ids": ",".join(coin_ids) if coin_ids else None,
            "category": category,
            "sparkline": False,
        }

        # Remove None values
        params = {k: v for k, v in params.items() if v is not None}

        response = await self.client.get(url, params=params)
        response.raise_for_status()
        market_data = response.json()

        # Fetch CAD prices separately if needed
        if len(vs_currencies) > 1 and "cad" in vs_currencies:
            cad_params = params.copy()
            cad_params["vs_currency"] = "cad"
            cad_response = await self.client.get(url, params=cad_params)
            cad_response.raise_for_status()
            cad_data = cad_response.json()

            # Merge CAD prices into main data
            cad_dict = {coin["id"]: coin for coin in cad_data}
            for coin in market_data:
                if coin["id"] in cad_dict:
                    coin["current_price_cad"] = cad_dict[coin["id"]]["current_price"]
                    coin["market_cap_cad"] = cad_dict[coin["id"]]["market_cap"]

        return market_data

    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()


# Global service instance
coingecko_service = CoinGeckoService()

