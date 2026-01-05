"""
Polymarket API Integration Module
Handles fetching market data from Polymarket's public API
"""
import requests
from typing import List, Dict, Optional


class PolymarketAPI:
    """Client for interacting with Polymarket's public API"""

    def __init__(self, base_url: str = "https://gamma-api.polymarket.com"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'application/json',
            'User-Agent': 'KalshiPolymarketComparisonTool/1.0'
        })

    def get_markets(self, limit: int = 200, active: bool = True, closed: bool = False) -> List[Dict]:
        """
        Fetch markets from Polymarket

        Args:
            limit: Maximum number of markets to return
            active: Include active markets
            closed: Include closed markets

        Returns:
            List of market dictionaries
        """
        endpoint = f"{self.base_url}/markets"
        params = {
            "limit": limit,
            "active": str(active).lower(),
            "closed": str(closed).lower()
        }

        try:
            response = self.session.get(endpoint, params=params, timeout=15)
            response.raise_for_status()
            markets = response.json()

            # Handle both list and dict responses
            if isinstance(markets, dict):
                markets = markets.get("data", [])

            print(f"✓ Fetched {len(markets)} Polymarket markets")
            return markets

        except requests.exceptions.Timeout:
            print("⚠ Polymarket API timeout")
            return []
        except requests.exceptions.RequestException as e:
            print(f"⚠ Polymarket API error: {e}")
            return []
        except Exception as e:
            print(f"⚠ Unexpected error fetching Polymarket markets: {e}")
            return []

    def get_event_markets(self, slug: str) -> Optional[Dict]:
        """
        Get markets for a specific event

        Args:
            slug: Event slug identifier

        Returns:
            Event data dictionary or None if error
        """
        endpoint = f"{self.base_url}/events/{slug}"

        try:
            response = self.session.get(endpoint, timeout=10)
            response.raise_for_status()
            return response.json()

        except requests.RequestException as e:
            print(f"⚠ Error fetching event {slug}: {e}")
            return None

    def format_event_link(self, market_data: Dict) -> str:
        """
        Generate direct link to Polymarket event page

        Args:
            market_data: Market dictionary with slug, event_slug, condition_id

        Returns:
            URL to event/market page
        """
        slug = market_data.get("slug", "")
        event_slug = market_data.get("event_slug", "")
        condition_id = market_data.get("condition_id", "")

        # For multi-market events, use event_slug/market_slug format
        if event_slug and slug and event_slug != slug:
            return f"https://polymarket.com/event/{event_slug}/{slug}"
        # For single-market events or standalone markets
        elif slug:
            return f"https://polymarket.com/event/{slug}"
        # Fallback to condition_id
        elif condition_id:
            return f"https://polymarket.com/event/{condition_id}"
        else:
            return "https://polymarket.com"

    def extract_market_info(self, market: Dict) -> Dict:
        """
        Extract relevant information from raw market data

        Args:
            market: Raw market dictionary from API

        Returns:
            Cleaned market information
        """
        # Try to get price from different possible fields
        outcome_prices = market.get("outcomePrices", market.get("outcome_prices", []))

        # Parse price (outcome_prices might be a JSON string or array)
        yes_price = 0.0
        if outcome_prices:
            try:
                # If it's a string, parse it as JSON
                if isinstance(outcome_prices, str):
                    import json
                    outcome_prices = json.loads(outcome_prices)

                # Now extract first price
                if isinstance(outcome_prices, list) and len(outcome_prices) > 0:
                    yes_price = float(outcome_prices[0])
            except (ValueError, TypeError, json.JSONDecodeError) as e:
                yes_price = 0.0

        # Get question/title
        question = market.get("question", market.get("title", market.get("description", "")))

        # Get slug for link - use only the slug field from API
        slug = market.get("slug", "")

        # Get event_slug if this market is part of a multi-market event
        event_slug = ""
        events = market.get("events", [])
        if events and len(events) > 0:
            event_slug = events[0].get("slug", "")

        # Get volume (handle different field names)
        volume = market.get("volume", market.get("volume24hr", market.get("volumeNum", 0)))
        try:
            volume = float(volume) if volume else 0
        except (ValueError, TypeError):
            volume = 0

        # Get liquidity
        liquidity = market.get("liquidity", market.get("liquidityNum", 0))
        try:
            liquidity = float(liquidity) if liquidity else 0
        except (ValueError, TypeError):
            liquidity = 0

        return {
            "condition_id": market.get("conditionId", ""),
            "slug": slug,
            "event_slug": event_slug,
            "question": question,
            "description": market.get("description", ""),
            "category": market.get("category", ""),
            "yes_price": yes_price,
            "no_price": 1 - yes_price if yes_price else 0,
            "volume": volume,
            "liquidity": liquidity,
            "end_date": market.get("endDate", market.get("end_date_iso", "")),
            "active": market.get("active", True),
            "closed": market.get("closed", False),
            "icon": market.get("icon", market.get("image", "")),
        }
