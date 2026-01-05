Comprehensive Prompt for Building a Kalshi vs Polymarket Comparison Tool

  ---
  Role Assignment

  You are an expert full-stack developer AI with deep expertise in building financial technology
  applications, data visualization dashboards, API integrations, and real-time market comparison
  tools. Your specialty includes working with prediction market platforms, handling asynchronous
  data fetching, implementing semantic matching algorithms, and creating intuitive user interfaces
   for traders and researchers. You understand regulatory compliance considerations, responsible
  gambling messaging, and best practices for building tools that handle financial data. You are
  proficient in modern web development frameworks, backend API development, data processing
  libraries, and have experience working with both centralized and decentralized platforms.

  ---
  Project Goal

  Your mission is to build a comprehensive, production-ready web application (or command-line tool
   with optional web interface) that compares similar prediction markets between Kalshi (a
  CFTC-regulated US prediction market platform) and Polymarket (a decentralized prediction market
  on Polygon blockchain). The application must:

  1. Fetch real-time market data from both platforms using their public APIs
  2. Intelligently match similar markets across platforms using semantic similarity, keyword
  matching, or topic categorization
  3. Display side-by-side comparisons showing prices/odds, implied probabilities, trading volumes,
   liquidity metrics, and bid/ask spreads
  4. Identify potential arbitrage opportunities where price discrepancies exist for equivalent
  events
  5. Provide direct clickable links to each market on the respective platform, enabling users to
  immediately navigate to trade or place bets
  6. Support search and filtering by topic, keyword, event category (politics, sports, crypto,
  etc.), or time period
  7. Update data in real-time or near-real-time using polling, websockets, or periodic refresh
  mechanisms
  8. Include educational content about each platform's unique characteristics, regulatory status,
  and risk disclaimers

  The final deliverable should be deployable (locally or to cloud platforms like Vercel, Netlify,
  or Heroku), well-documented, and maintainable by developers with moderate technical skills.

  ---
  Essential Background Research on Kalshi and Polymarket

  Before you begin implementation, understand these critical details about each platform:

  Kalshi Platform Overview

  Kalshi is the first CFTC-regulated prediction market exchange in the United States, allowing
  legal event contracts on outcomes ranging from politics and elections to sports, cryptocurrency
  prices, weather events, economic indicators, and cultural phenomena. Key characteristics:

  - Regulatory Status: CFTC-regulated as a Designated Contract Market (DCM), making it legally
  compliant for US users
  - Market Structure: Operates as a centralized order book exchange with binary event contracts
  (Yes/No outcomes)
  - Pricing: Prices are quoted in cents ($0.01 to $0.99), where the price directly represents
  implied probability (e.g., 65 cents = 65% probability)
  - API Access: Comprehensive public REST API documented at https://docs.kalshi.com with endpoints
   for market data, orderbooks, trade history, and event metadata
  - Market Links: Markets are accessible via URLs formatted as https://kalshi.com/markets/{ticker}
   (example: https://kalshi.com/markets/TRUMPWIN24 for a Trump election win market)
  - Developer Resources:
    - Quick Start Guide: https://docs.kalshi.com/getting_started/quick_start_market_data
    - Markets API Documentation: https://docs.kalshi.com/typescript-sdk/api/MarketsApi
    - Python SDK: Install via pip install kalshi-python for simplified integration
    - TypeScript SDK: Available for Node.js/browser applications
    - Builder Grants Program: $2M+ in funding available at https://kalshi.com/builders for
  developers building on Kalshi
    - Builder Codes: Volume-based revenue sharing program allowing developers to monetize
  applications
    - GitHub Tools: https://github.com/Kalshi/tools-and-analysis contains analysis scripts and
  examples
  - Key API Endpoints (no authentication required for public data):
    - GET /markets - List all available markets with filters
    - GET /markets/{market_id} - Detailed market information including current prices
    - GET /markets/{market_id}/orderbook - Real-time bid/ask order book
    - GET /markets/{market_id}/history - Historical price data
  - Partnerships: Integrations with Coinbase, Solana ecosystem, and various trading platforms
  - Social Media: Follow @Kalshi and @KalshiEco on X (Twitter) for platform updates, new markets,
  and builder announcements

  Polymarket Platform Overview

  Polymarket is a decentralized prediction market platform built on Polygon (Ethereum Layer 2),
  offering peer-to-peer betting on real-world events with cryptocurrency. Key characteristics:

  - Regulatory Status: Operates as a decentralized platform; previously settled CFTC charges in
  2022, currently restricts US IP addresses but accessible globally
  - Market Structure: Uses an automated market maker (AMM) and order book hybrid model with USDC
  as the base currency
  - Pricing: Prices range from $0.00 to $1.00, representing probability (e.g., $0.72 = 72%
  probability)
  - API Access: GraphQL API documented at https://docs.polymarket.com with extensive query
  capabilities
  - Event Links: Markets are grouped under events accessible via
  https://polymarket.com/event/{slug} (example:
  https://polymarket.com/event/will-donald-trump-win-the-2024-us-presidential-election)
  - Developer Resources:
    - API Overview: https://docs.polymarket.com/developers/gamma-markets-api/overview
    - Get Markets Endpoint: https://docs.polymarket.com/developers/CLOB/markets/get-markets
    - Developer Resources Hub: https://docs.polymarket.com/developers/dev-resources/main
    - Liquidity Incentives: https://docs.polymarket.com/developers/rewards/overview - rewards for
  market makers
    - Builder Program: https://docs.polymarket.com/developers/builders/builder-intro for ecosystem
   integrations
    - Jupyter Notebooks/Gists: Community-created onboarding materials like
  https://gist.github.com/shaunlebron/0dd3338f7dea06b8e9f8724981bb13bf
  - Key API Endpoints (GraphQL):
    - GET /markets - Query all markets with filtering
    - GET /events - Event groups containing multiple related markets
    - Real-time subscriptions available for live price updates
    - Order book and trade history endpoints
  - Partnerships: MetaMask integration, NYSE/ICE investment backing, various DeFi protocol
  integrations
  - Historical Accuracy: Platform claims 94% accuracy in predictions compared to actual outcomes
  - Social Media: Follow @Polymarket on X for market launches, accuracy reports, and platform
  updates

  Platform Comparison Considerations

  When building the comparison tool, note these critical differences:

  1. Regulatory: Kalshi is US-regulated and legal for US users; Polymarket blocks US IPs but
  operates globally
  2. Currency: Kalshi uses USD; Polymarket uses USDC (stablecoin)
  3. Market Creation: Kalshi curates markets internally; Polymarket allows permissionless market
  creation (within guidelines)
  4. Liquidity Sources: Kalshi has centralized liquidity; Polymarket combines AMM and order books
  5. Settlement: Kalshi settles through regulated process; Polymarket uses oracle-based smart
  contract settlement
  6. User Base: Different geographic distributions and trading cultures

  ---
  Key Features - Detailed Requirements

  Implement the following features with high attention to detail:

  1. Data Fetching and API Integration

  Kalshi Integration:
  - Use the public REST API (no authentication initially) to fetch market data
  - Implement calls to GET /markets with category filters (politics, sports, crypto, etc.)
  - For each matched market, fetch detailed data including current Yes/No prices, volume, open
  interest, expiration date
  - Retrieve orderbook data to calculate bid-ask spreads and liquidity depth
  - Handle rate limiting gracefully (implement exponential backoff if needed)
  - Parse market tickers and titles to extract event semantics

  Polymarket Integration:
  - Use GraphQL API to query markets and events
  - Fetch market prices (both outcomes), volume, liquidity pool sizes, number of traders
  - Query event metadata including descriptions, resolution sources, and end dates
  - Extract market slugs for generating direct links
  - Handle pagination for large result sets
  - Implement error handling for network failures or API changes

  Shared Requirements:
  - Cache API responses appropriately to minimize redundant calls
  - Implement retry logic for failed requests
  - Log API errors for debugging
  - Support both one-time fetching and periodic updates (every 30-60 seconds for real-time mode)

  2. Market Matching Algorithm

  Since markets on different platforms won't have identical names or identifiers, implement
  intelligent matching:

  Semantic Matching Options:
  - Keyword Extraction: Parse market titles to extract key entities (names, dates, numerical
  thresholds, event types)
  - Topic Categorization: Group markets by category (US elections, crypto prices, sports outcomes,
   weather)
  - Similarity Scoring: Use libraries like spaCy, sentence-transformers, or simple TF-IDF cosine
  similarity to compute semantic similarity between market descriptions
  - Manual Curation: Allow users to manually link markets or provide a curated mapping file

  Example Matching Logic:
  - Kalshi market: "Will Bitcoin exceed $100,000 by Dec 31, 2024?"
  - Polymarket event: "Bitcoin above $100k on December 31, 2024?"
  - Match criteria: Both mention "Bitcoin", "$100k" threshold, and "Dec 31, 2024" date

  Edge Cases:
  - Handle differently worded but equivalent outcomes (e.g., "Trump wins 2024 election" vs "Trump
  elected President 2024")
  - Manage inverted outcomes (Yes on one platform = No on another if questions are framed
  oppositely)
  - Flag uncertain matches with confidence scores

  3. User Interface and Data Visualization

  Core Display Components:

  Market Comparison Table:
  - Side-by-side columns for Kalshi and Polymarket
  - Rows showing: Market Title, Current Price (Yes/No), Implied Probability %, Trading Volume
  (24h/total), Liquidity/Open Interest, Bid-Ask Spread, Last Updated timestamp
  - Color-coded probability differences (green if Kalshi > Polymarket, red if opposite)
  - Arbitrage opportunity indicator (highlight when price discrepancy exceeds threshold, e.g.,
  >5%)

  Direct Market Links:
  - Each market row must include clickable buttons/links labeled "Trade on Kalshi" and "Trade on
  Polymarket"
  - Links must redirect to the exact market page using proper URL formats:
    - Kalshi: https://kalshi.com/markets/{ticker}
    - Polymarket: https://polymarket.com/event/{slug}
  - Open links in new tabs to preserve comparison view

  Search and Filtering:
  - Search bar to filter markets by keyword (e.g., "Trump", "Bitcoin", "Super Bowl")
  - Category dropdown/tabs for Politics, Sports, Crypto, Weather, Economics, etc.
  - Date range filter for market expiration/resolution dates
  - Toggle for showing only markets with arbitrage opportunities

  Real-Time Updates:
  - Display last refresh timestamp
  - Auto-refresh toggle (enable/disable periodic updates)
  - Visual indicator when data is being fetched (loading spinner)

  Educational Sidebar:
  - Brief explanations of how prediction markets work
  - Differences between Kalshi and Polymarket (regulation, geography, settlement)
  - Risk warnings: "Prediction markets involve financial risk. Only bet what you can afford to
  lose."
  - Disclaimer: "This tool is for informational purposes only and does not constitute financial
  advice."

  Responsive Design:
  - Mobile-friendly layout that collapses comparison into stacked cards on small screens
  - Accessible color schemes (WCAG AA compliant)
  - Fast load times even with many markets displayed

  4. Arbitrage Detection and Alerts

  Calculation Logic:
  - For matched markets, compute probability difference: |P_kalshi - P_polymarket|
  - Flag opportunities where difference exceeds configurable threshold (default 5-10%)
  - Consider transaction costs, platform fees, and withdrawal times when assessing true
  profitability
  - Display potential profit assuming equal bet size on both sides (basic arbitrage calculator)

  Alert Mechanisms (Optional Enhancement):
  - Browser notifications when new arbitrage opportunities appear
  - Email/webhook alerts for users who want push notifications
  - Historical tracking of arbitrage frequency and duration

  5. Error Handling and Edge Cases

  Robust Error Management:
  - Handle API downtime gracefully with cached fallback data
  - Display user-friendly error messages ("Unable to fetch Kalshi data, retrying...")
  - Log technical errors to console for debugging
  - Validate API responses before processing (check for expected fields)

  Edge Cases to Handle:
  - Markets suspended or closed on one platform but active on another
  - Differences in outcome formatting (binary vs multi-outcome markets)
  - Time zone discrepancies in expiration dates
  - Currency conversion if displaying volumes in standardized units
  - Empty result sets (no matching markets found)

  6. Compliance and Responsible Use

  Risk Disclaimers:
  - Prominent notice that prediction markets are not available to all jurisdictions
  - Warning about Polymarket's US IP blocking and Kalshi's US-only operation
  - Statement: "This comparison tool does not endorse or promote gambling. Users must comply with
  local laws."

  No Automation of Trades:
  - Tool should only display information and links, not execute trades automatically
  - Clearly state this is a comparison/research tool, not a trading bot

  Data Accuracy:
  - Include timestamp on all data points
  - Note that prices change rapidly and displayed data may be slightly delayed
  - Encourage users to verify prices on platforms before trading

  ---
  Technical Requirements and Implementation Guidance

  Recommended Technology Stack

  Option 1: Python Backend + Streamlit Frontend (Easiest for rapid development)
  - Backend: Python 3.9+ with requests library for API calls, pandas for data processing
  - Market Matching: spaCy or scikit-learn for semantic similarity
  - Frontend: Streamlit for quick interactive dashboard
  - Deployment: Streamlit Cloud or Heroku
  - Pros: Fast to build, easy to iterate, Python SDKs available for Kalshi
  - Cons: Less customizable UI, may not scale to thousands of users

  Option 2: Node.js Backend + React Frontend (Production-grade)
  - Backend: Express.js server with node-fetch or axios for APIs
  - Market Matching: Natural library or simple keyword parsing
  - Frontend: React with Material-UI or Tailwind CSS for styling
  - Real-time: Use polling or Socket.io for live updates
  - Deployment: Vercel (frontend) + Heroku/Railway (backend) or full-stack on single platform
  - Pros: Highly customizable, scalable, good for complex features
  - Cons: More code to write, longer development time

  Option 3: Full-Stack Next.js (Modern approach)
  - Framework: Next.js 14+ with App Router
  - API Routes: Server-side API calls in Next.js API routes or Server Components
  - Frontend: React components with server-side rendering for performance
  - Deployment: Vercel (optimized for Next.js)
  - Pros: Best performance, SEO-friendly, single codebase
  - Cons: Requires Next.js expertise

  Choose the stack based on your strengths and project timeline. For this prompt, we'll focus on
  Option 1 (Python + Streamlit) as the primary approach, but you can adapt to other stacks.

  Step-by-Step Implementation Guide

  Step 1: Environment Setup

  # Create project directory
  mkdir kalshi-polymarket-comparison
  cd kalshi-polymarket-comparison

  # Create virtual environment
  python -m venv venv
  source venv/bin/activate  # On Windows: venv\Scripts\activate

  # Install dependencies
  pip install kalshi-python requests streamlit pandas numpy spacy python-dotenv

  # Download spaCy language model for semantic matching
  python -m spacy download en_core_web_md

  Create .env file for configuration (optional, for future API keys):
  KALSHI_API_BASE=https://api.kalshi.com/trade-api/v2
  POLYMARKET_API_BASE=https://gamma-api.polymarket.com
  REFRESH_INTERVAL=60

  Step 2: Build Kalshi Data Fetcher

  Create kalshi_api.py:

  import requests
  from typing import List, Dict, Optional

  class KalshiAPI:
      def __init__(self, base_url="https://api.kalshi.com/trade-api/v2"):
          self.base_url = base_url

      def get_markets(self, category: Optional[str] = None, limit: int = 100) -> List[Dict]:
          """Fetch markets from Kalshi public API"""
          endpoint = f"{self.base_url}/markets"
          params = {"limit": limit, "status": "open"}
          if category:
              params["category"] = category

          try:
              response = requests.get(endpoint, params=params, timeout=10)
              response.raise_for_status()
              data = response.json()
              return data.get("markets", [])
          except requests.RequestException as e:
              print(f"Kalshi API error: {e}")
              return []

      def get_market_details(self, ticker: str) -> Optional[Dict]:
          """Get detailed market info including orderbook"""
          try:
              # Market details
              market_response = requests.get(
                  f"{self.base_url}/markets/{ticker}",
                  timeout=10
              )
              market_data = market_response.json()

              # Orderbook for liquidity
              orderbook_response = requests.get(
                  f"{self.base_url}/markets/{ticker}/orderbook",
                  timeout=10
              )
              orderbook_data = orderbook_response.json()

              return {
                  "market": market_data.get("market"),
                  "orderbook": orderbook_data.get("orderbook")
              }
          except requests.RequestException as e:
              print(f"Error fetching {ticker}: {e}")
              return None

      def format_market_link(self, ticker: str) -> str:
          """Generate direct link to Kalshi market"""
          return f"https://kalshi.com/markets/{ticker}"

  Step 3: Build Polymarket Data Fetcher

  Create polymarket_api.py:

  import requests
  from typing import List, Dict, Optional

  class PolymarketAPI:
      def __init__(self, base_url="https://gamma-api.polymarket.com"):
          self.base_url = base_url

      def get_markets(self, limit: int = 100, active: bool = True) -> List[Dict]:
          """Fetch markets from Polymarket"""
          endpoint = f"{self.base_url}/markets"
          params = {"limit": limit, "active": active}

          try:
              response = requests.get(endpoint, params=params, timeout=10)
              response.raise_for_status()
              return response.json()
          except requests.RequestException as e:
              print(f"Polymarket API error: {e}")
              return []

      def get_event_markets(self, slug: str) -> Optional[Dict]:
          """Get markets for a specific event"""
          try:
              response = requests.get(
                  f"{self.base_url}/events/{slug}",
                  timeout=10
              )
              response.raise_for_status()
              return response.json()
          except requests.RequestException as e:
              print(f"Error fetching event {slug}: {e}")
              return None

      def format_event_link(self, slug: str) -> str:
          """Generate direct link to Polymarket event"""
          return f"https://polymarket.com/event/{slug}"

  Step 4: Implement Market Matching Logic

  Create market_matcher.py:

  import spacy
  from typing import List, Dict, Tuple
  import re

  class MarketMatcher:
      def __init__(self):
          # Load spaCy model for semantic similarity
          try:
              self.nlp = spacy.load("en_core_web_md")
          except:
              print("spaCy model not found, using keyword matching only")
              self.nlp = None

      def extract_keywords(self, text: str) -> set:
          """Extract important keywords from market title"""
          # Remove common words and extract entities
          text_lower = text.lower()
          # Extract dates, numbers, names
          keywords =
  set(re.findall(r'\b(?:\d{4}|trump|biden|bitcoin|btc|eth|election|super\s+bowl|\$\d+k?)\b',
  text_lower))
          return keywords

      def compute_similarity(self, market1: Dict, market2: Dict) -> float:
          """Compute similarity score between two markets (0-1)"""
          title1 = market1.get("title", "")
          title2 = market2.get("title", "")

          # Keyword-based matching
          keywords1 = self.extract_keywords(title1)
          keywords2 = self.extract_keywords(title2)

          if not keywords1 or not keywords2:
              return 0.0

          keyword_overlap = len(keywords1 & keywords2) / max(len(keywords1), len(keywords2))

          # Semantic similarity if spaCy available
          if self.nlp:
              doc1 = self.nlp(title1)
              doc2 = self.nlp(title2)
              semantic_sim = doc1.similarity(doc2)
              # Average keyword and semantic similarity
              return (keyword_overlap + semantic_sim) / 2

          return keyword_overlap

      def find_matches(self, kalshi_markets: List[Dict], poly_markets: List[Dict], threshold: 
  float = 0.6) -> List[Tuple[Dict, Dict, float]]:
          """Find matching markets across platforms"""
          matches = []

          for k_market in kalshi_markets:
              best_match = None
              best_score = 0

              for p_market in poly_markets:
                  score = self.compute_similarity(k_market, p_market)
                  if score > best_score and score >= threshold:
                      best_score = score
                      best_match = p_market

              if best_match:
                  matches.append((k_market, best_match, best_score))

          return sorted(matches, key=lambda x: x[2], reverse=True)

  Step 5: Build Streamlit Dashboard

  Create app.py:

  import streamlit as st
  import pandas as pd
  from kalshi_api import KalshiAPI
  from polymarket_api import PolymarketAPI
  from market_matcher import MarketMatcher
  import time

  # Page config
  st.set_page_config(
      page_title="Kalshi vs Polymarket Comparison",
      page_icon="📊",
      layout="wide"
  )

  # Initialize APIs
  @st.cache_resource
  def init_apis():
      return KalshiAPI(), PolymarketAPI(), MarketMatcher()

  kalshi_api, poly_api, matcher = init_apis()

  # Title and description
  st.title("📊 Kalshi vs Polymarket Market Comparison")
  st.markdown("""
  Compare prediction markets side-by-side between **Kalshi** (CFTC-regulated, US-only) and 
  **Polymarket** (decentralized, global). 
  Find arbitrage opportunities and get direct links to trade.

  **⚠️ Risk Warning**: Prediction markets involve financial risk. This tool is for informational 
  purposes only. 
  Verify all prices on platforms before trading. Not available in all jurisdictions.
  """)

  # Sidebar controls
  st.sidebar.header("Filters")
  categories = st.sidebar.multiselect(
      "Categories",
      ["Politics", "Sports", "Crypto", "Economics", "Weather"],
      default=["Politics", "Crypto"]
  )

  search_query = st.sidebar.text_input("Search markets", "")
  arbitrage_only = st.sidebar.checkbox("Show only arbitrage opportunities (>5% diff)")
  auto_refresh = st.sidebar.checkbox("Auto-refresh (60s)")

  # Fetch data
  @st.cache_data(ttl=60)
  def fetch_markets():
      with st.spinner("Fetching markets from Kalshi and Polymarket..."):
          kalshi_markets = kalshi_api.get_markets(limit=200)
          poly_markets = poly_api.get_markets(limit=200)
          matches = matcher.find_matches(kalshi_markets, poly_markets, threshold=0.5)
      return matches

  if st.sidebar.button("Refresh Data") or auto_refresh:
      st.cache_data.clear()

  matches = fetch_markets()

  # Filter matches
  filtered_matches = matches
  if search_query:
      filtered_matches = [
          m for m in matches
          if search_query.lower() in m[0].get("title", "").lower()
          or search_query.lower() in m[1].get("title", "").lower()
      ]

  if arbitrage_only:
      filtered_matches = [
          m for m in filtered_matches
          if abs(m[0].get("yes_price", 0) - m[1].get("outcome_prices", [0])[0]) > 0.05
      ]

  # Display results
  st.subheader(f"Found {len(filtered_matches)} matching markets")

  for k_market, p_market, similarity in filtered_matches:
      col1, col2, col3 = st.columns([2, 2, 1])

      with col1:
          st.markdown(f"**🏛️ Kalshi**: {k_market.get('title')}")
          k_price = k_market.get("yes_price", 0)
          st.metric("Yes Price", f"${k_price:.2f}", f"{k_price*100:.1f}%")
          st.link_button("Trade on Kalshi", kalshi_api.format_market_link(k_market.get("ticker")))

      with col2:
          st.markdown(f"**🔗 Polymarket**: {p_market.get('question')}")
          p_price = p_market.get("outcome_prices", [0])[0]
          st.metric("Yes Price", f"${p_price:.2f}", f"{p_price*100:.1f}%")
          st.link_button("Trade on Polymarket", poly_api.format_event_link(p_market.get("slug")))

      with col3:
          diff = abs(k_price - p_price) * 100
          st.metric("Price Diff", f"{diff:.1f}%",
                   delta_color="inverse" if diff > 5 else "normal")
          if diff > 5:
              st.warning("⚡ Arbitrage!")

      st.divider()

  # Footer with resources
  st.sidebar.markdown("---")
  st.sidebar.markdown("""
  ### Learn More
  - [Kalshi API Docs](https://docs.kalshi.com)
  - [Polymarket API Docs](https://docs.polymarket.com)
  - [Builder Programs](https://kalshi.com/builders)

  **Platform Differences:**
  - **Kalshi**: CFTC-regulated, USD, US-only
  - **Polymarket**: Decentralized, USDC, global (blocks US IPs)
  """)

  if auto_refresh:
      time.sleep(60)
      st.rerun()

  Step 6: Testing and Deployment

  Local Testing:
  streamlit run app.py

  Deployment to Streamlit Cloud:
  1. Push code to GitHub repository
  2. Go to share.streamlit.io
  3. Connect repository and select app.py
  4. Add requirements.txt:
  streamlit
  kalshi-python
  requests
  pandas
  spacy
  python-dotenv
  5. Deploy and share public URL

  Alternative Deployments:
  - Heroku: Use Procfile with web: streamlit run app.py --server.port=$PORT
  - Docker: Create Dockerfile for containerized deployment
  - Vercel/Netlify: Requires adaptation to serverless functions

  Real-Time Updates Implementation

  For production real-time updates, consider:

  1. Polling (Simplest): Set ttl=60 in @st.cache_data for 60-second cache expiration
  2. WebSockets: Use Socket.io if APIs support websocket subscriptions (Polymarket has this
  capability)
  3. Server-Sent Events (SSE): Push updates from backend to frontend
  4. Background Worker: Use Celery or similar to fetch data periodically and cache in Redis

  Rate Limiting Considerations

  Both APIs have rate limits:
  - Kalshi: Typically allows generous public data access; consider caching responses
  - Polymarket: Implement backoff if you hit limits (usually 100-300 requests/min)

  Implement exponential backoff:
  import time
  from functools import wraps

  def retry_with_backoff(max_retries=3):
      def decorator(func):
          @wraps(func)
          def wrapper(*args, **kwargs):
              for attempt in range(max_retries):
                  try:
                      return func(*args, **kwargs)
                  except requests.HTTPError as e:
                      if e.response.status_code == 429:  # Rate limit
                          wait_time = 2 ** attempt
                          time.sleep(wait_time)
                      else:
                          raise
              return None
          return wrapper
      return decorator

  ---
  Output Format Instructions

  Your final deliverable should include:

  1. Complete Source Code: All Python files (or your chosen language) with comprehensive inline
  comments
  2. README.md: Installation instructions, usage guide, API key setup (if needed), deployment
  steps
  3. requirements.txt (or package.json): All dependencies with versions
  4. Configuration Guide: How to customize categories, matching thresholds, refresh intervals
  5. Architecture Documentation: Brief explanation of how components interact (data flow diagram
  optional but helpful)
  6. Sample Output: Screenshots or descriptions of what users will see
  7. Testing Guide: How to verify the tool works correctly
  8. Known Limitations: Document edge cases, API limitations, or features not yet implemented

  Code Quality Standards:
  - Follow PEP 8 (Python) or relevant style guide for your language
  - Use type hints where applicable
  - Handle errors gracefully with try-except blocks
  - Log important events and errors
  - Comment complex logic
  - Make code modular and reusable

  Documentation Structure:
  kalshi-polymarket-comparison/
  ├── README.md
  ├── requirements.txt
  ├── .env.example
  ├── app.py (main Streamlit app)
  ├── kalshi_api.py
  ├── polymarket_api.py
  ├── market_matcher.py
  ├── utils/
  │   ├── arbitrage.py
  │   └── formatting.py
  ├── tests/
  │   └── test_matching.py
  └── docs/
      ├── ARCHITECTURE.md
      └── API_REFERENCE.md

  ---
  Edge Cases and Enhancements

  Critical Edge Cases to Handle

  1. Inverted Market Outcomes: If Kalshi asks "Will X happen?" and Polymarket asks "Will X NOT
  happen?", the Yes price on one = No price on the other. Detect and invert prices accordingly.
  2. Multi-Outcome Markets: Polymarket often has multiple outcomes (e.g., "Trump wins", "Biden
  wins", "Other"). Kalshi typically binary. Match only binary equivalents or handle multi-outcome
  carefully.
  3. Market Suspension: Markets can close or suspend suddenly. Display status clearly and disable
  links if closed.
  4. Different Time Zones: Normalize all timestamps to UTC and display user's local time.
  5. Stale Data: Show age of data prominently. Flag data older than 5 minutes as potentially
  stale.
  6. API Schema Changes: APIs can change structure. Validate expected fields exist before
  accessing them.
  7. Network Failures: If one API is down, still display data from the working one with a notice.
  8. Empty Results: If no matches found, provide helpful message suggesting broader search or
  category selection.

  Optional Enhancements

  Advanced Features (implement if time allows):

  1. Historical Price Charts: Use Chart.js or Plotly to show price movements over time for matched
   markets
  2. User Authentication: Allow users to save favorite markets or get personalized alerts
  3. Advanced Arbitrage Calculator: Input bet amounts and compute exact profit accounting for
  fees, slippage, withdrawal costs
  4. Market News Integration: Pull relevant news articles or social media posts about events
  5. Probability Aggregation: Combine probabilities from both platforms into a meta-prediction
  6. Mobile App: Convert to React Native or Flutter for iOS/Android
  7. Browser Extension: Chrome/Firefox extension that overlays comparison data on
  Kalshi/Polymarket sites
  8. Telegram/Discord Bot: Alert bot that pushes arbitrage opportunities to chat channels
  9. Export Functionality: Download comparison data as CSV or JSON for external analysis
  10. Community Curation: Allow users to manually link markets that automated matching missed
  11. Backtesting: Show historical arbitrage opportunities and how long they lasted
  12. Multi-Platform Support: Extend to include PredictIt, Betfair, or other prediction markets

  Performance Optimizations:
  - Implement database caching (SQLite, PostgreSQL, or Redis) for market data
  - Use async/await for concurrent API calls (Python asyncio or JavaScript promises)
  - Paginate results for large datasets
  - Lazy load market details on user interaction instead of fetching everything upfront

  Accessibility Improvements:
  - Keyboard navigation support
  - Screen reader compatibility (ARIA labels)
  - High contrast mode
  - Adjustable font sizes

  ---
  Additional Research Resources for Reference

  Use these links for deeper research if you need clarification or updated information:

  Kalshi Resources:
  - API Quick Start: https://docs.kalshi.com/getting_started/quick_start_market_data
  - Markets API Reference: https://docs.kalshi.com/typescript-sdk/api/MarketsApi
  - Builder Program: https://kalshi.com/builders
  - GitHub Tools: https://github.com/Kalshi/tools-and-analysis
  - X/Twitter: @Kalshi, @KalshiEco

  Polymarket Resources:
  - API Overview: https://docs.polymarket.com/developers/gamma-markets-api/overview
  - Get Markets Endpoint: https://docs.polymarket.com/developers/CLOB/markets/get-markets
  - Developer Resources: https://docs.polymarket.com/developers/dev-resources/main
  - Liquidity Incentives: https://docs.polymarket.com/developers/rewards/overview
  - Builder Program: https://docs.polymarket.com/developers/builders/builder-intro
  - Data API Gists: https://gist.github.com/shaunlebron/0dd3338f7dea06b8e9f8724981bb13bf
  - X/Twitter: @Polymarket

  Community and Comparisons:
  - Reddit Discussion on Comparison Tools: https://www.reddit.com/r/Kalshi/comments/1jot30p/kalshi
  polymarket_market_comparison_tool_looking/
  - General Prediction Market Forums: Search for "Kalshi Polymarket comparison" on Reddit, Discord
   servers, or Twitter

  Technical Documentation:
  - spaCy for NLP: https://spacy.io/usage/linguistic-features#similarity
  - Streamlit Docs: https://docs.streamlit.io
  - React Documentation (if using React): https://react.dev
  - GraphQL Queries: https://graphql.org/learn/queries/

  ---
  Final Instructions and Expectations

  1. Begin Implementation: Start coding immediately based on the architecture outlined above. Use
  the provided code snippets as starting points and expand them to full functionality.
  2. Research When Needed: If you encounter API endpoints or parameters not fully documented here,
   use the provided links to research current API specifications. APIs evolve, so verify endpoint
  paths and response schemas.
  3. Prioritize Core Features First: Build in this order:
    - Basic API fetching from both platforms
    - Simple keyword-based matching
    - Minimal UI showing side-by-side comparison
    - Direct links to markets
    - Then add: semantic matching, arbitrage detection, real-time updates, advanced filtering
  4. Test Thoroughly: Verify that:
    - API calls return expected data
    - Market matching produces reasonable pairs
    - Links redirect correctly to live markets
    - Error handling works (try disconnecting internet)
    - UI is responsive on mobile devices
  5. Document Everything: Write README as if for a developer who has never seen the project.
  Include:
    - What the project does (overview)
    - How to install and run locally
    - How to deploy to production
    - How to contribute or extend features
    - Credits and license information
  6. Comply with Legal Requirements: Include all necessary disclaimers about financial risk,
  jurisdictional restrictions, and tool limitations. Never suggest this tool guarantees profit or
  is without risk.
  7. Provide Complete Code: Output the full, functional codebase—not pseudocode or incomplete
  snippets. The code should run successfully after following setup instructions.
  8. Explain Design Decisions: In your documentation or comments, briefly justify why you chose
  specific technologies, algorithms, or approaches (e.g., "Used spaCy for semantic matching
  because it provides pre-trained models and good accuracy for short text similarity").
  9. Include Sample Data (Optional): If APIs are unavailable during development, include mock JSON
   responses for testing purposes.
  10. Future Roadmap: Suggest 3-5 features that could be added in future iterations to make this a
   more comprehensive tool.

  ---
  Expected Outcome

  Upon completion, you will have delivered a fully functional, deployable web application or
  dashboard that:

  - Connects to Kalshi and Polymarket APIs without requiring user authentication for public data
  - Intelligently matches similar prediction markets across platforms using automated algorithms
  - Displays real-time (or near-real-time) price comparisons, volumes, and implied probabilities
  - Provides direct, clickable links to each platform's market pages for immediate trading access
  - Highlights potential arbitrage opportunities with visual indicators
  - Includes search, filtering, and categorization for easy market discovery
  - Features a clean, responsive user interface that works on desktop and mobile
  - Contains comprehensive documentation and deployment instructions
  - Adheres to legal and ethical standards with appropriate risk disclaimers

  This tool will serve traders, researchers, and prediction market enthusiasts who want to compare
   markets across platforms, discover pricing inefficiencies, and make informed decisions based on
   comprehensive market data.

  Now begin development. Good luck, and build something exceptional!