# Kalshi vs Polymarket Market Comparison Tool

A comprehensive web application that compares prediction markets between **Kalshi** (CFTC-regulated US platform) and **Polymarket** (decentralized global platform). Find arbitrage opportunities, compare prices, and get direct links to trade.

## 🎯 Features

- **Real-time Market Comparison**: Fetch and compare markets from both platforms
- **Intelligent Matching**: Automatically matches similar markets using keyword and semantic analysis
- **Arbitrage Detection**: Highlights price discrepancies >5% for potential arbitrage opportunities
- **Direct Trading Links**: Click-through to exact market pages on both platforms
- **Search & Filtering**: Find markets by keyword, category, or minimum match score
- **Auto-refresh**: Optional 60-second auto-refresh for real-time monitoring
- **Educational Content**: Platform differences, risk warnings, and resource links

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)

### Installation

1. **Clone or navigate to the project directory**:
   ```bash
   cd /Users/mac/Documents/claude/poly66
   ```

2. **Create and activate virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. **Activate virtual environment** (if not already activated):
   ```bash
   source venv/bin/activate
   ```

2. **Run Streamlit app**:
   ```bash
   streamlit run app.py
   ```

3. **Open your browser** to the URL shown (typically `http://localhost:8501`)

## 📁 Project Structure

```
poly66/
├── app.py                  # Main Streamlit application
├── kalshi_api.py          # Kalshi API integration
├── polymarket_api.py      # Polymarket API integration
├── market_matcher.py      # Market matching algorithm
├── requirements.txt       # Python dependencies
├── .env.example          # Example environment variables
├── README_PROJECT.md     # This file
└── readme.md             # Original project specification
```

## 🔧 Configuration

No API keys are required for public market data. The application uses:

- **Kalshi API**: `https://api.kalshi.com/trade-api/v2`
- **Polymarket API**: `https://gamma-api.polymarket.com`

You can optionally create a `.env` file based on `.env.example` to customize API endpoints.

## 📊 How It Works

### 1. Data Fetching

- **Kalshi**: Fetches up to 200 open markets using public REST API
- **Polymarket**: Fetches up to 200 active markets using public API
- Both APIs are accessed without authentication for public data

### 2. Market Matching

The matching algorithm:
- Extracts keywords from market titles (names, dates, numbers, thresholds)
- Computes similarity using Jaccard index on keyword sets
- Matches each Kalshi market with the most similar Polymarket market
- Filters by minimum similarity threshold (default 30%)

### 3. Arbitrage Detection

- Calculates price difference between matched markets
- Flags opportunities where difference exceeds 5%
- Displays suggested arbitrage direction (buy low, sell high)
- **Note**: Actual profitability depends on fees, slippage, and withdrawal times

### 4. Display

- Side-by-side market comparison
- Real-time price probabilities
- Volume and liquidity metrics
- Direct links to trading pages
- Match confidence scores

## 🎨 User Interface

### Main Features

- **Search Bar**: Filter markets by keyword (e.g., "Trump", "Bitcoin")
- **Similarity Slider**: Adjust minimum match score (10%-90%)
- **Arbitrage Filter**: Show only markets with >5% price difference
- **Auto-refresh**: Enable 60-second automatic data refresh
- **Market Cards**: Expandable details with volume, liquidity, status

### Sidebar Information

- Platform statistics (total markets, matches found)
- Arbitrage opportunity count
- Last updated timestamp
- Educational resources
- Platform comparison guide

## ⚠️ Important Disclaimers

### Risk Warning

**Prediction markets involve financial risk. This tool is for informational purposes only.**

- Not financial advice
- Prices change rapidly
- Data may be delayed
- Verify prices before trading
- Transaction fees apply
- Withdrawal times vary
- Not available in all jurisdictions

### Platform Restrictions

- **Kalshi**: Legal only for US users (CFTC-regulated)
- **Polymarket**: Blocks US IP addresses (accessible globally otherwise)

### No Trade Execution

This tool **does not** execute trades. It only:
- Displays information
- Provides comparison data
- Links to official platforms

Users must manually verify and execute trades on the respective platforms.

## 🛠️ Technical Details

### API Endpoints Used

**Kalshi**:
- `GET /markets` - List markets with filters
- `GET /markets/{ticker}` - Market details
- `GET /markets/{ticker}/orderbook` - Order book data

**Polymarket**:
- `GET /markets` - List markets
- `GET /events/{slug}` - Event details

### Rate Limiting

- Kalshi: Generous public data access, recommended caching
- Polymarket: ~100-300 requests/min, built-in retry logic
- App uses 60-second cache TTL to minimize API calls

### Error Handling

- Graceful API timeout handling (15-second timeout)
- Fallback to cached data when available
- User-friendly error messages
- Detailed logging for debugging

## 🔍 Matching Algorithm Details

### Keyword Extraction

Identifies important keywords including:
- **Politics**: trump, biden, election, president, senate, etc.
- **Crypto**: bitcoin, ethereum, btc, eth, price, etc.
- **Sports**: nfl, nba, super bowl, mvp, championship, etc.
- **Economics**: gdp, inflation, fed, rate, recession, etc.
- **Numbers**: Years (2024, 2025), dollar amounts ($100k), percentages

### Similarity Scoring

- Jaccard similarity on keyword sets
- Category matching bonus (+10% if same category)
- Fallback to word overlap if no keywords found
- Score range: 0.0 (no match) to 1.0 (perfect match)

### Edge Cases Handled

- Different wording for same event
- Inverted questions (Yes on one = No on other)
- Multi-outcome vs binary markets
- Closed/suspended markets
- Missing data fields

## 📈 Future Enhancements

Potential features for future versions:

1. **Historical Price Charts**: Show price movements over time
2. **Advanced Arbitrage Calculator**: Account for fees, slippage, withdrawal costs
3. **User Authentication**: Save favorites, custom alerts
4. **Market News Integration**: Relevant news articles per market
5. **Mobile App**: React Native or Flutter version
6. **Browser Extension**: Overlay comparison on Kalshi/Polymarket sites
7. **Telegram/Discord Bot**: Push arbitrage alerts
8. **Multi-platform Support**: Add PredictIt, Betfair, etc.
9. **Database Caching**: PostgreSQL/Redis for better performance
10. **Semantic Matching**: spaCy or sentence-transformers for better similarity

## 🤝 Contributing

This is an educational project. To extend functionality:

1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Test thoroughly
5. Submit pull request

## 📄 License

Educational and research use only. Not licensed for commercial use.

## 🙏 Credits

Built using:
- [Streamlit](https://streamlit.io) - Web framework
- [Kalshi API](https://docs.kalshi.com) - Market data
- [Polymarket API](https://docs.polymarket.com) - Market data
- [Requests](https://requests.readthedocs.io) - HTTP client
- [Pandas](https://pandas.pydata.org) - Data processing

## 📞 Support

For issues or questions:
- Review the documentation at official platform sites
- Check API status pages
- Verify your internet connection
- Ensure you're using Python 3.9+

## ⚖️ Compliance

Users must:
- Comply with local laws and regulations
- Verify platform availability in their jurisdiction
- Understand financial risks
- Not use this tool for automated trading
- Verify all data before making financial decisions

---

**Disclaimer**: This comparison tool does not endorse or promote gambling. Use responsibly and at your own risk.
