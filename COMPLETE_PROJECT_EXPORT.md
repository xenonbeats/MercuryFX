# MercuryFX V2 - Complete Project Export
**Generated:** August 20, 2025  
**Status:** Production Ready with Advanced Risk Management

## 📁 Project Files

### 1. main.py - Flask Server Entry Point
```python
import os
import threading
import logging
from dotenv import load_dotenv
from flask import Flask, render_template
from trading_bot import TradingBot

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('mercuryfx.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "mercuryfx_default_secret")

# Global bot instance
bot = None

@app.route('/')
def index():
    """Health check endpoint for UptimeRobot monitoring"""
    return "MercuryFX V2 Bot is alive!", 200

@app.route('/status')
def status():
    """Status page with bot information"""
    return render_template('index.html')

def start_trading_bot():
    """Start the trading bot in a separate thread"""
    global bot
    try:
        bot = TradingBot()
        bot.start()
    except Exception as e:
        logger.error(f"Failed to start trading bot: {e}")

if __name__ == '__main__':
    # Start the trading bot in a separate thread
    bot_thread = threading.Thread(target=start_trading_bot, daemon=True)
    bot_thread.start()
    
    logger.info("Starting MercuryFX V2 Flask server on port 5000")
    
    # Start Flask server
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
```

### 2. requirements.txt - Dependencies
```
email-validator
flask
flask-sqlalchemy
gunicorn
numpy
pandas
pandas-ta
psycopg2-binary
python-dotenv
python-telegram-bot
requests
ta
ta-lib
yfinance
```

### 3. .env.example - Environment Variables Template
```bash
# Telegram Configuration
TELEGRAM_TOKEN=your_telegram_bot_token_here
CHAT_ID=your_telegram_chat_id_here

# Flask Configuration (optional)
SESSION_SECRET=your_random_session_secret
```

## 🚀 Installation Instructions

### Step 1: Clone/Create Project
1. Create new directory: `mkdir mercuryfx_v2`
2. Copy all files to the directory
3. Navigate to directory: `cd mercuryfx_v2`

### Step 2: Install Dependencies
```bash
# Using pip
pip install -r requirements.txt

# Using uv (Replit)
uv add yfinance pandas pandas-ta requests flask python-dotenv python-telegram-bot ta ta-lib numpy gunicorn
```

### Step 3: Configure Environment
1. Copy `.env.example` to `.env`
2. Get Telegram Bot Token from @BotFather
3. Get Chat ID from your Telegram channel/chat
4. Update `.env` with your tokens

### Step 4: Run the Bot
```bash
# Development
python main.py

# Production (Replit)
gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app
```

## 📊 Key Features

### Smart Money Concepts (SMC)
- Break of Structure (BOS) detection
- Market Structure Shift (MSS) identification  
- Fair Value Gap (FVG) analysis
- Order Block recognition
- Advanced liquidity analysis

### Risk Management System
- ATR-based volatility analysis
- Support/resistance level detection
- Optimal stop loss placement
- Multi-level take profit targets
- Position size optimization
- Risk validation (minimum 2:1 R/R)

### Signal Quality Control
- 75% minimum confidence threshold
- Multi-indicator confluence required
- Volatility screening
- Asset-specific filtering
- High-quality sniper strategy

### Telegram Integration
- Concise signal format with vital info only
- Multiple take profit levels
- Risk assessment and lot size recommendations
- Real-time notifications
- Error handling and status updates

## 📈 Performance Enhancements

### Recent Improvements (August 2025)
1. **Advanced Risk Management**: Added ATR volatility analysis and optimal SL/TP placement
2. **Support/Resistance Detection**: Smart level identification for better entry/exit points  
3. **Enhanced Signal Filtering**: Strict quality control to avoid poor risk setups
4. **Multi-Level Take Profits**: TP1, TP2, TP3 for progressive profit taking
5. **Position Size Optimization**: Calculated optimal lot sizes based on risk percentage

### Signal Success Metrics
- Minimum 2:1 Risk/Reward ratio
- Target 2.5:1+ for high-quality setups
- 75%+ confidence threshold
- Multi-pattern SMC confluence required

## 🔧 Customization Options

### Adjustable Parameters
- Confidence threshold (default: 75%)
- Risk/reward minimum (default: 2:1)
- Monitoring interval (default: 15 minutes)
- ATR period (default: 14)
- Swing point strength (default: 5)

### Adding New Assets
Update `symbols` dictionary in `trading_bot.py`:
```python
'SYMBOL': {
    'name': 'Asset Name',
    'atr_multiplier': 0.002,  # Adjust based on asset
    'asset_type': 'forex'     # forex/crypto/commodity
}
```

## 🛡️ Security Notes
- Never commit `.env` file to version control
- Use environment variables for all sensitive data
- Regularly rotate API tokens
- Monitor bot activity through Telegram notifications

## 📱 Monitoring & Maintenance
- Health check endpoint: `http://your-domain/`
- Status page: `http://your-domain/status`
- Logs stored in `mercuryfx.log`
- UptimeRobot integration ready

## 🎯 Trade Management Guidelines
1. **Demo Testing**: Always test new setups on demo first
2. **Risk Control**: Never risk more than 1-2% per trade
3. **Position Sizing**: Use calculated lot sizes from bot
4. **Take Profits**: Consider scaling out at multiple TP levels
5. **Stop Loss**: Never move SL against position

## 📞 Support
- Check logs for error details
- Verify environment variables are set correctly
- Ensure sufficient market data is available
- Monitor Telegram bot token validity

---

**MercuryFX V2** - Advanced SMC Trading Signal Bot
*Built with sophisticated risk management and quality control*