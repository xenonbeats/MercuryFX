# MercuryFX V2 - Multi-Strategy Trading Signal Bot

## Project Overview
MercuryFX V2 is a Python-based multi-strategy trading signal bot for forex and cryptocurrency markets. The bot monitors multiple assets, calculates technical indicators, and sends trading signals via Telegram.

## Project Architecture

### Core Components
- **Market Data**: Uses yfinance to fetch real-time data for EURUSD, GBPUSD, XAUUSD, and BTC-USD
- **Smart Money Concepts (SMC)**: Advanced analysis including BOS, MSS, FVG, and Order Blocks
- **Technical Analysis**: EMA50, EMA200, RSI(14), and MACD using TA-Lib library
- **Risk Management**: Multi-layer filtering with SMC-based SL/TP calculation
- **Telegram Integration**: Enhanced signal formatting with SMC confluence data

### Advanced Signal Logic (SMC Sniper Strategy)
- **High-Quality Filtering**: Only signals with 75%+ confidence are sent
- **SMC Confluence**: Requires 2+ Smart Money Concepts patterns
- **Traditional Confirmation**: RSI, EMA, MACD must align with SMC direction
- **Volatility Screening**: Avoids choppy markets and major news events
- **Asset-Specific Rules**: Customized filters for Forex, Commodity, and Crypto

### Smart Money Concepts (SMC)
1. **Break of Structure (BOS)**: Continuation patterns - price breaking previous swing highs/lows
2. **Market Structure Shift (MSS)**: Reversal patterns - trend change confirmations
3. **Fair Value Gap (FVG)**: Price imbalances showing institutional interest
4. **Order Blocks**: Supply/demand zones where institutions placed large orders

### Traditional Technical Indicators
1. **EMA50 vs EMA200**: Trend direction (more conservative thresholds)
2. **RSI(14)**: Momentum (35/65 levels instead of 30/70 for better quality)
3. **MACD**: Trend changes with zero-line confirmation

## Dependencies
- yfinance: Market data retrieval
- pandas: Data manipulation
- numpy: Numerical calculations
- python-telegram-bot: Telegram integration
- python-dotenv: Environment variables
- ta: Technical analysis indicators

## User Preferences
- **Strategy**: SMC Sniper approach with BOS, MSS, FVG, Order Block analysis
- **Quality Focus**: Only high-confidence setups (75%+ threshold) to avoid poor risk trades
- **Monitoring interval**: 15 minutes with advanced filtering
- **Assets**: EUR/USD, GBP/USD, Gold (XAU/USD), Bitcoin (BTC-USD)
- **Risk Management**: SMC-based SL/TP with 2.5:1 reward ratios for quality setups
- **Signal Philosophy**: Skip low-quality setups entirely - no notifications for poor risk trades

## Recent Changes
- 2025-08-20: Initial project setup with dependencies installed
- 2025-08-20: Core architecture defined for multi-strategy signal generation
- 2025-08-20: Flask web server implemented with health endpoint for UptimeRobot
- 2025-08-20: Telegram integration completed and tested successfully
- 2025-08-20: Bot fully operational with environment variables configured
- 2025-08-20: Technical analysis using TA-Lib library for reliable indicator calculations
- 2025-08-20: **MAJOR UPGRADE**: Integrated Smart Money Concepts (SMC) analysis
- 2025-08-20: Added advanced filtering system - only high-quality sniper setups are posted
- 2025-08-20: Enhanced Telegram messages with SMC confluence and risk quality metrics
- 2025-08-20: Implemented volatility screening and asset-specific quality checks
- 2025-08-20: Updated Telegram signal format to concise version with vital info only (Entry, SL, multiple TP levels, lot sizes, risk assessment)
- 2025-08-20: **MAJOR RISK UPGRADE**: Added advanced risk management with ATR volatility analysis, support/resistance detection, optimal SL/TP placement, and position sizing optimization after $139 demo loss