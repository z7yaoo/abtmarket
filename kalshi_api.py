"""
Kalshi API Integration Module
Handles fetching market data from Kalshi's public API
"""
import requests
from typing import List, Dict, Optional
import time


class KalshiAPI:
    """Client for interacting with Kalshi's public API"""

    def __init__(self, base_url: str = "https://api.elections.kalshi.com/trade-api/v2"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'application/json',
            'User-Agent': 'KalshiPolymarketComparisonTool/1.0'
        })

    def get_markets(self, category: Optional[str] = None, limit: int = 200, status: str = "open") -> List[Dict]:
        """
        Fetch events with nested markets (real prices + working URLs)

        Args:
            category: Filter by category (e.g., 'politics', 'crypto')
            limit: Maximum number of events to return
            status: Event status ('open', 'closed', etc.)

        Returns:
            List of market dictionaries with real prices AND working URLs
        """
        endpoint = f"{self.base_url}/events"
        params = {
            "limit": limit,
            "status": status,
            "with_nested_markets": "true"
        }

        if category:
            params["series_ticker"] = category

        try:
            response = self.session.get(endpoint, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
            events = data.get("events", [])

            # Extract markets from events and add series_ticker for URLs
            all_markets = []
            for event in events:
                series_ticker = event.get('series_ticker')
                markets = event.get('markets', [])

                # Add series_ticker to each market for URL generation
                for market in markets:
                    market['series_ticker'] = series_ticker
                    all_markets.append(market)

            print(f"✓ Fetched {len(all_markets)} markets from {len(events)} events")
            return all_markets

        except requests.exceptions.Timeout:
            print("⚠ Kalshi API timeout")
            return []
        except requests.exceptions.RequestException as e:
            print(f"⚠ Kalshi API error: {e}")
            return []
        except Exception as e:
            print(f"⚠ Unexpected error fetching Kalshi markets: {e}")
            return []

    def get_market_details(self, ticker: str) -> Optional[Dict]:
        """
        Get detailed market info including orderbook

        Args:
            ticker: Market ticker symbol

        Returns:
            Dictionary with market and orderbook data, or None if error
        """
        try:
            # Fetch market details
            market_url = f"{self.base_url}/markets/{ticker}"
            market_response = self.session.get(market_url, timeout=10)
            market_response.raise_for_status()
            market_data = market_response.json()

            # Small delay to avoid rate limiting
            time.sleep(0.1)

            # Fetch orderbook
            orderbook_url = f"{self.base_url}/markets/{ticker}/orderbook"
            orderbook_response = self.session.get(orderbook_url, timeout=10)
            orderbook_response.raise_for_status()
            orderbook_data = orderbook_response.json()

            return {
                "market": market_data.get("market", {}),
                "orderbook": orderbook_data.get("orderbook", {})
            }

        except requests.RequestException as e:
            print(f"⚠ Error fetching details for {ticker}: {e}")
            return None

    def format_market_link(self, market_data: Dict) -> str:
        """
        Generate direct link to Kalshi event page using series_ticker

        Args:
            market_data: Dict with 'series_ticker', 'ticker', or 'event_ticker'

        Returns:
            URL to Kalshi event page
        """
        # Prefer series_ticker for direct event URLs
        series_ticker = market_data.get('series_ticker', '').lower()
        if series_ticker:
            return f"https://kalshi.com/markets/{series_ticker}"

        # Fallback to ticker
        ticker = market_data.get('ticker', '').lower()
        if ticker:
            return f"https://kalshi.com/markets/{ticker}"

        # Final fallback: homepage
        return "https://kalshi.com"

    def extract_market_info(self, market: Dict) -> Dict:
        """
        Extract relevant information from raw market data

        Args:
            market: Raw market dictionary from API

        Returns:
            Cleaned market information
        """
        # Get yes price with fallback logic
        yes_price = 0.0

        try:
            # Try last_price_dollars first (most recent trade)
            last_price = market.get("last_price_dollars")
            if last_price and float(last_price) > 0:
                yes_price = float(last_price)
            else:
                # Try midpoint of bid/ask
                yes_bid = float(market.get("yes_bid_dollars", 0.0) or 0.0)
                yes_ask = float(market.get("yes_ask_dollars", 0.0) or 0.0)

                if yes_bid > 0 and yes_ask > 0:
                    yes_price = (yes_bid + yes_ask) / 2
                elif yes_ask > 0:
                    yes_price = yes_ask
                elif yes_bid > 0:
                    yes_price = yes_bid
        except (ValueError, TypeError):
            yes_price = 0.0

        # Calculate no_price
        no_price = 1.0 - yes_price if yes_price > 0 else 0.0

        return {
            "ticker": market.get("ticker", ""),
            "event_ticker": market.get("event_ticker", ""),
            "series_ticker": market.get("series_ticker", ""),
            "mve_collection_ticker": market.get("mve_collection_ticker", ""),
            "title": market.get("title", ""),
            "subtitle": market.get("subtitle", ""),
            "category": market.get("category", ""),
            "status": market.get("status", ""),
            "yes_price": yes_price,
            "no_price": no_price,
            "volume": market.get("volume", 0),
            "open_interest": market.get("open_interest", 0),
            "close_time": market.get("close_time", ""),
            "result": market.get("result", ""),
        }
