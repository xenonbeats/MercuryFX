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
