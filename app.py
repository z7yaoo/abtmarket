"""
MarketParity - Market Comparison Tool
Main Streamlit Application
"""
import streamlit as st
import pandas as pd
from datetime import datetime
import time

from kalshi_api import KalshiAPI
from polymarket_api import PolymarketAPI
from market_matcher import MarketMatcher


# Page configuration
st.set_page_config(
    page_title="MarketParity - Market Comparison",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Professional Dark Mode with Glassmorphism
st.markdown("""
<style>
    /* Import Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@300;400;500;600;700&family=Poppins:wght@400;500;600;700;800&display=swap');

    /* Hide Streamlit Header/Toolbar - Multiple selectors for compatibility */
    header[data-testid="stHeader"],
    div[data-testid="stToolbar"],
    div[data-testid="stDecoration"],
    div[data-testid="stStatusWidget"],
    #MainMenu,
    header,
    footer {
        visibility: hidden !important;
        height: 0 !important;
        position: fixed !important;
        top: -100px !important;
    }

    /* Force hide via multiple methods */
    iframe[title="streamlit_option_menu.nav_item"] {
        display: none !important;
    }

    /* Reduce top padding */
    .main .block-container {
        padding-top: 1rem !important;
        max-width: 100% !important;
    }

    /* Remove Streamlit branding */
    footer {
        visibility: hidden !important;
    }

    footer:after {
        content: '';
        visibility: hidden;
        display: block;
    }

    /* Global Styles - Dark Mode */
    .stApp {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        font-family: 'Open Sans', sans-serif;
    }

    /* Typography */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Poppins', sans-serif !important;
        color: #F8FAFC !important;
        font-weight: 700 !important;
    }

    h1 {
        background: linear-gradient(135deg, #F59E0B 0%, #FBBF24 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.5rem !important;
        margin-bottom: 1rem !important;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.95) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(51, 65, 85, 0.3);
    }

    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #F59E0B !important;
    }

    /* Glass Cards */
    .element-container {
        margin-bottom: 1rem;
    }

    div[data-testid="column"] {
        background: rgba(30, 41, 59, 0.6);
        backdrop-filter: blur(16px);
        border-radius: 16px;
        border: 1px solid rgba(51, 65, 85, 0.5);
        padding: 1.5rem;
        transition: all 200ms ease;
    }

    div[data-testid="column"]:hover {
        background: rgba(30, 41, 59, 0.8);
        border-color: rgba(245, 158, 11, 0.3);
        transform: translateY(-2px);
        box-shadow: 0 8px 32px rgba(245, 158, 11, 0.15);
    }

    /* Metrics */
    [data-testid="stMetric"] {
        background: rgba(15, 23, 42, 0.5);
        padding: 1rem;
        border-radius: 12px;
        border: 1px solid rgba(51, 65, 85, 0.4);
    }

    [data-testid="stMetricLabel"] {
        color: #94A3B8 !important;
        font-size: 0.875rem !important;
        font-weight: 500 !important;
    }

    [data-testid="stMetricValue"] {
        color: #F8FAFC !important;
        font-size: 1.875rem !important;
        font-weight: 700 !important;
        font-family: 'Poppins', sans-serif !important;
    }

    /* Buttons */
    .stButton button {
        background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 100%);
        color: #FFFFFF;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        font-size: 0.875rem;
        transition: all 200ms ease;
        box-shadow: 0 4px 14px rgba(139, 92, 246, 0.3);
    }

    .stButton button:hover {
        background: linear-gradient(135deg, #7C3AED 0%, #6D28D9 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(139, 92, 246, 0.4);
    }

    /* Link Buttons */
    a[data-testid="stButton"] {
        text-decoration: none !important;
    }

    /* Alerts */
    .stAlert {
        background: rgba(245, 158, 11, 0.1);
        border: 1px solid rgba(245, 158, 11, 0.3);
        border-radius: 12px;
        color: #FBBF24 !important;
        padding: 1rem;
    }

    /* Arbitrage Alert */
    .stSuccess {
        background: rgba(34, 197, 94, 0.1) !important;
        border-color: rgba(34, 197, 94, 0.3) !important;
        color: #4ADE80 !important;
    }

    .stWarning {
        background: rgba(245, 158, 11, 0.1) !important;
        border-color: rgba(245, 158, 11, 0.3) !important;
        color: #FBBF24 !important;
    }

    .stError {
        background: rgba(239, 68, 68, 0.1) !important;
        border-color: rgba(239, 68, 68, 0.3) !important;
        color: #F87171 !important;
    }

    /* Input Fields */
    input, textarea, select {
        background: rgba(15, 23, 42, 0.8) !important;
        border: 1px solid rgba(51, 65, 85, 0.5) !important;
        border-radius: 12px !important;
        color: #F8FAFC !important;
        padding: 0.75rem !important;
        transition: all 200ms ease !important;
    }

    input:focus, textarea:focus {
        border-color: #F59E0B !important;
        box-shadow: 0 0 0 3px rgba(245, 158, 11, 0.1) !important;
    }

    /* Checkbox */
    .stCheckbox {
        color: #F8FAFC !important;
    }

    /* Divider */
    hr {
        border-color: rgba(51, 65, 85, 0.3) !important;
        margin: 2rem 0 !important;
    }

    /* Text Colors */
    p, span, div {
        color: #CBD5E1 !important;
    }

    strong {
        color: #F8FAFC !important;
        font-weight: 600 !important;
    }

    /* Links */
    a {
        color: #8B5CF6 !important;
        transition: color 200ms ease !important;
    }

    a:hover {
        color: #A78BFA !important;
    }

    /* Spinner */
    .stSpinner > div {
        border-color: #F59E0B transparent transparent transparent !important;
    }

    /* Custom Market Card Classes */
    .market-card-arbitrage {
        border: 2px solid rgba(239, 68, 68, 0.5) !important;
        background: rgba(239, 68, 68, 0.05) !important;
        animation: pulse 2s ease-in-out infinite;
    }

    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.9; }
    }

    /* Platform Headers */
    .platform-header {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }

    .kalshi-header {
        background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%);
        color: white;
    }

    .polymarket-header {
        background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 100%);
        color: white;
    }

    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }

    ::-webkit-scrollbar-track {
        background: rgba(15, 23, 42, 0.5);
    }

    ::-webkit-scrollbar-thumb {
        background: rgba(245, 158, 11, 0.5);
        border-radius: 5px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: rgba(245, 158, 11, 0.7);
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def init_apis():
    """Initialize API clients (cached)"""
    return KalshiAPI(), PolymarketAPI(), MarketMatcher()


# Temporarily removed cache to test
# @st.cache_data(ttl=60)
def fetch_markets(_kalshi_api, _poly_api, _matcher, search_query="", min_similarity=0.5, _version="v2"):
    """
    Fetch and match markets from both platforms

    Args:
        _kalshi_api: KalshiAPI instance
        _poly_api: PolymarketAPI instance
        _matcher: MarketMatcher instance
        search_query: Search filter
        min_similarity: Minimum similarity threshold
        _version: Cache version (change to invalidate cache)

    Returns:
        List of matched markets
    """
    with st.spinner("🔄 Fetching markets from Kalshi and Polymarket..."):
        # Fetch from both platforms (Kalshi max limit is 200)
        kalshi_raw = _kalshi_api.get_markets(limit=200)
        poly_raw = _poly_api.get_markets(limit=500)

        # Extract market info from both platforms
        kalshi_markets = [_kalshi_api.extract_market_info(m) for m in kalshi_raw]
        poly_markets = [_poly_api.extract_market_info(m) for m in poly_raw]

        # Filter out markets with no price data
        kalshi_markets = [m for m in kalshi_markets if m.get("yes_price", 0) > 0]
        poly_markets = [m for m in poly_markets if m.get("yes_price", 0) > 0]

        # Note: No need to filter categorical Kalshi markets anymore
        # Algorithm uses Polymarket as source and won't match generic "Who/Which/What"
        # questions with specific Polymarket markets (proper noun mismatch)

        # Filter by search query if provided
        if search_query:
            search_lower = search_query.lower()
            kalshi_markets = [
                m for m in kalshi_markets
                if search_lower in m.get("title", "").lower()
            ]
            poly_markets = [
                m for m in poly_markets
                if search_lower in m.get("question", "").lower()
            ]

        # Find matches
        matches = _matcher.find_matches(kalshi_markets, poly_markets, threshold=min_similarity)

        return matches, len(kalshi_markets), len(poly_markets)


def display_market_card(market, platform, similarity, price_diff_pct, api_instance):
    """
    Display a single market card in grid layout using Streamlit components

    Args:
        market: Market dict
        platform: "kalshi" or "polymarket"
        similarity: Match similarity score
        price_diff_pct: Price difference percentage
        api_instance: API instance for link generation
    """
    is_kalshi = platform == "kalshi"
    price = market.get("yes_price", 0)
    prob = price * 100
    vol = market.get('volume', 0)

    # Get title and category
    title = market.get('title' if is_kalshi else 'question', 'N/A')
    category = market.get('category', 'Other')

    # Check arbitrage
    is_arbitrage = price_diff_pct > 5

    # Container with colored border
    border_class = "🟡" if is_arbitrage else ""

    with st.container():
        # Platform badge and category in columns
        badge_col, cat_col = st.columns([3, 1])
        with badge_col:
            if is_kalshi:
                st.markdown("**🏛️ KALSHI**")
            else:
                st.markdown("**🔗 POLYMARKET**")
        with cat_col:
            st.caption(category)

        # Title
        st.markdown(f"**{title[:100]}**")

        # Probability display
        prob_col1, prob_col2 = st.columns([2, 1])
        with prob_col1:
            st.caption("Current Probability")
        with prob_col2:
            st.markdown(f"### {prob:.0f}%")

        # Progress bar
        st.progress(int(prob) if prob <= 100 else 100)

        # Volume and Match Score
        vol_match_col1, vol_match_col2 = st.columns(2)
        with vol_match_col1:
            st.caption(f"Volume: **${vol:,.0f}**")
        with vol_match_col2:
            # Color code similarity: green (good), yellow (ok), red (poor)
            if similarity >= 0.7:
                st.caption(f"✅ Match: **{similarity*100:.0f}%**")
            elif similarity >= 0.5:
                st.caption(f"⚠️ Match: **{similarity*100:.0f}%**")
            else:
                st.caption(f"❌ Match: **{similarity*100:.0f}%**")

        # Arbitrage indicator
        if is_arbitrage:
            st.warning(f"⚡ {price_diff_pct:.1f}% SPREAD")

        # Buttons
        btn_cols = st.columns(2)

        # Generate link
        if is_kalshi:
            link = api_instance.format_market_link(market)
        else:
            link = api_instance.format_event_link(market)

        # Use unique key
        if is_kalshi:
            unique_id = f"{market.get('ticker', '')}_{market.get('event_ticker', '')}"
        else:
            unique_id = f"{market.get('condition_id', '')}_{market.get('slug', '')}"

        with btn_cols[0]:
            st.button("View Details", key=f"view_{platform}_{hash(unique_id)}", use_container_width=True, disabled=True)

        with btn_cols[1]:
            st.link_button("Trade Now", link, use_container_width=True)


def display_market_comparison(k_market, p_market, similarity, kalshi_api, poly_api):
    """
    Display matched market pair as two cards side by side

    Args:
        k_market: Kalshi market dict
        p_market: Polymarket market dict
        similarity: Similarity score
        kalshi_api: KalshiAPI instance
        poly_api: PolymarketAPI instance
    """
    # Calculate price difference
    k_price = k_market.get("yes_price", 0)
    p_price = p_market.get("yes_price", 0)
    price_diff = abs(k_price - p_price)
    price_diff_pct = price_diff * 100

    # Create two columns
    col1, col2 = st.columns(2)

    with col1:
        display_market_card(k_market, "kalshi", similarity, price_diff_pct, kalshi_api)

    with col2:
        display_market_card(p_market, "polymarket", similarity, price_diff_pct, poly_api)


def main():
    """Main application function"""

    # Initialize APIs
    kalshi_api, poly_api, matcher = init_apis()

    # Hero Header
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.15) 0%, rgba(245, 158, 11, 0.15) 100%);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 32px;
        margin-bottom: 24px;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    ">
        <h1 style="
            background: linear-gradient(135deg, #F59E0B 0%, #FBBF24 50%, #8B5CF6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 2.5em;
            margin: 0 0 16px 0;
            font-weight: 800;
        ">
            ⚖️ MarketParity
        </h1>
        <p style="color: #CBD5E1; font-size: 1.2em; margin: 0; line-height: 1.6;">
            Compare prediction markets side-by-side • Find arbitrage opportunities • Trade with one click
        </p>
        <div style="margin-top: 20px; display: flex; gap: 16px; justify-content: center; flex-wrap: wrap;">
            <span style="
                background: rgba(16, 185, 129, 0.2);
                color: #6EE7B7;
                padding: 8px 16px;
                border-radius: 20px;
                font-size: 0.9em;
                font-weight: 600;
            ">🏛️ Kalshi - CFTC Regulated</span>
            <span style="
                background: rgba(139, 92, 246, 0.2);
                color: #C4B5FD;
                padding: 8px 16px;
                border-radius: 20px;
                font-size: 0.9em;
                font-weight: 600;
            ">🔗 Polymarket - Decentralized</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Risk Warning
    st.markdown("""
    <div style="
        background: rgba(245, 158, 11, 0.1);
        border-left: 4px solid #F59E0B;
        border-radius: 8px;
        padding: 16px 20px;
        margin-bottom: 24px;
    ">
        <p style="color: #FDE68A; margin: 0; font-size: 0.95em;">
            <strong>⚠️ Risk Warning:</strong> Prediction markets involve financial risk. This tool is for informational
            purposes only. Verify all prices on platforms before trading. Not available in all jurisdictions.
            Arbitrage opportunities may disappear quickly and include transaction costs, fees, and withdrawal delays.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar controls
    st.sidebar.markdown("""
    <div style="
        background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 100%);
        color: white;
        padding: 16px;
        border-radius: 12px;
        margin-bottom: 20px;
        text-align: center;
        font-weight: 700;
        font-size: 1.1em;
        box-shadow: 0 4px 16px rgba(139, 92, 246, 0.3);
    ">
        🔍 Filters & Settings
    </div>
    """, unsafe_allow_html=True)

    # Search
    search_query = st.sidebar.text_input(
        "Search markets",
        placeholder="e.g., Trump, Bitcoin, Super Bowl",
        help="Filter markets by keyword"
    )

    # Similarity threshold
    min_similarity = st.sidebar.slider(
        "Minimum Match Score",
        min_value=0.1,
        max_value=0.9,
        value=0.1,
        step=0.1,
        help="Higher values show only more similar matches (recommended: 0.5-0.7 for accurate arbitrage)"
    )

    # Arbitrage filter
    arbitrage_only = st.sidebar.checkbox(
        "Show only arbitrage opportunities (>5% diff)",
        value=False
    )

    # Auto-refresh
    auto_refresh = st.sidebar.checkbox(
        "Auto-refresh every 60 seconds",
        value=False
    )

    # Manual refresh button
    if st.sidebar.button("🔄 Refresh Data Now", type="primary", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

    # Fetch markets
    try:
        matches, kalshi_count, poly_count = fetch_markets(
            kalshi_api,
            poly_api,
            matcher,
            search_query=search_query,
            min_similarity=min_similarity,
            _version="v2"
        )

        # Stats
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 📈 Statistics")
        st.sidebar.metric("Kalshi Markets", kalshi_count)
        st.sidebar.metric("Polymarket Markets", poly_count)
        st.sidebar.metric("Matched Markets", len(matches))

        # Count arbitrage opportunities
        arbitrage_count = sum(
            1 for k, p, s in matches
            if abs(k.get("yes_price", 0) - p.get("yes_price", 0)) * 100 > 5
        )
        st.sidebar.metric("Arbitrage Opportunities", arbitrage_count)

        # Debug Info
        with st.sidebar.expander("🔍 Debug Info"):
            st.caption(f"**Markets Fetched:**")
            st.caption(f"• Kalshi: {kalshi_count} markets")
            st.caption(f"• Polymarket: {poly_count} markets")
            st.caption(f"")
            st.caption(f"**Matching Results:**")
            st.caption(f"• Matches found: {len(matches)}")
            match_rate = (len(matches) / kalshi_count * 100) if kalshi_count > 0 else 0
            st.caption(f"• Match rate: {match_rate:.1f}%")
            st.caption(f"• Similarity threshold: {min_similarity*100:.0f}%")
            st.caption(f"")
            st.caption(f"**Tip:** ถ้ามี match น้อยเกินไป ลอง:")
            st.caption(f"• ลด Similarity threshold")
            st.caption(f"• ปิด Arbitrage Only filter")

        # Last updated
        st.sidebar.caption(f"Last updated: {datetime.now().strftime('%H:%M:%S')}")

    except Exception as e:
        st.error(f"❌ Error fetching markets: {e}")
        st.stop()

    # Filter by arbitrage if needed
    if arbitrage_only:
        matches = [
            (k, p, s) for k, p, s in matches
            if abs(k.get("yes_price", 0) - p.get("yes_price", 0)) * 100 > 5
        ]

    # Display results
    st.markdown("<div style='height: 32px;'></div>", unsafe_allow_html=True)

    if len(matches) == 0:
        st.markdown("""
        <div style="
            background: rgba(59, 130, 246, 0.1);
            border: 1px solid rgba(59, 130, 246, 0.3);
            border-radius: 12px;
            padding: 24px;
            text-align: center;
        ">
            <p style="color: #93C5FD; font-size: 1.1em; margin: 0;">
                🔍 No matching markets found. Try adjusting your filters or search query.
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Get unique categories
        all_categories = set()
        for k_market, p_market, _ in matches:
            if k_market.get('category'):
                all_categories.add(k_market.get('category'))
            if p_market.get('category'):
                all_categories.add(p_market.get('category'))

        categories = ["All Markets"] + sorted(list(all_categories))

        # Category Filter
        st.markdown("""
        <div style="margin-bottom: 24px;">
            <h3 style="color: #E2E8F0; font-size: 0.9em; margin-bottom: 12px; font-weight: 600;">FILTER BY CATEGORY</h3>
        </div>
        """, unsafe_allow_html=True)

        # Create filter buttons
        selected_category = st.radio(
            "Category",
            categories,
            horizontal=True,
            label_visibility="collapsed",
            key="category_filter"
        )

        # Filter matches by category
        if selected_category != "All Markets":
            filtered_matches = [
                (k, p, s) for k, p, s in matches
                if k.get('category') == selected_category or p.get('category') == selected_category
            ]
        else:
            filtered_matches = matches

        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, rgba(245, 158, 11, 0.15) 0%, rgba(139, 92, 246, 0.15) 100%);
            border-radius: 12px;
            padding: 20px;
            margin: 24px 0;
            text-align: center;
        ">
            <h2 style="
                background: linear-gradient(135deg, #F59E0B 0%, #8B5CF6 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin: 0;
                font-size: 1.8em;
            ">
                🎯 {len(filtered_matches)} Markets {f'in {selected_category}' if selected_category != 'All Markets' else 'Found'}
            </h2>
        </div>
        """, unsafe_allow_html=True)

        # Display each match
        for k_market, p_market, similarity in filtered_matches:
            display_market_comparison(k_market, p_market, similarity, kalshi_api, poly_api)

    # Educational content in sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    ### 📚 Learn More

    **Platform Differences:**
    - **Kalshi**: CFTC-regulated, USD, US-only, centralized
    - **Polymarket**: Decentralized, USDC, global (blocks US IPs)

    **How Arbitrage Works:**
    When the same event has different prices on different platforms,
    you can potentially profit by buying low on one and selling high on the other.

    **⚠️ Important Notes:**
    - Prices change rapidly
    - Transaction fees apply
    - Withdrawal times vary
    - Regulatory restrictions apply
    - This tool does NOT execute trades
    """)

    # Footer
    st.markdown("---")
    st.caption("""
    🤖 Built for educational and research purposes only. Not financial advice.
    This comparison tool does not endorse or promote gambling. Users must comply with local laws.
    Data may be delayed. Always verify prices on official platforms before trading.
    """)

    # Auto-refresh logic
    if auto_refresh:
        time.sleep(60)
        st.rerun()


if __name__ == "__main__":
    main()
