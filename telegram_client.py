import os
import logging
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class TelegramClient:
    def __init__(self):
        """Initialize Telegram client"""
        self.token = os.getenv('TELEGRAM_TOKEN', 'default_token')
        self.chat_id = os.getenv('CHAT_ID', 'default_chat_id')
        self.base_url = f"https://api.telegram.org/bot{self.token}"
        
        if self.token == 'default_token':
            logger.warning("Using default Telegram token - please set TELEGRAM_TOKEN environment variable")
        if self.chat_id == 'default_chat_id':
            logger.warning("Using default chat ID - please set CHAT_ID environment variable")
        
        logger.info("TelegramClient initialized")
    
    def send_message(self, message):
        """Send a message to Telegram"""
        try:
            url = f"{self.base_url}/sendMessage"
            payload = {
                'chat_id': self.chat_id,
                'text': message,
                'parse_mode': 'HTML'
            }
            
            response = requests.post(url, json=payload, timeout=10)
            
            if response.status_code == 200:
                logger.debug("Message sent successfully to Telegram")
                return True
            else:
                logger.error(f"Failed to send message. Status: {response.status_code}, Response: {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Error sending Telegram message: {e}")
            return False
    
    def format_signal_message(self, signal):
        """Format concise trading signal for Telegram"""
        try:
            direction_emoji = "🟢 BUY" if signal['direction'] == 'BUY' else "🔴 SELL"
            asset_emoji = self.get_asset_emoji(signal['symbol'])
            
            # Calculate risk/reward ratio
            if signal['direction'] == 'BUY':
                risk = signal['entry_price'] - signal['stop_loss']
                reward = signal['take_profit'] - signal['entry_price']
            else:
                risk = signal['stop_loss'] - signal['entry_price']
                reward = signal['entry_price'] - signal['take_profit']
            
            rr_ratio = reward / risk if risk > 0 else 0
            
            # Calculate multiple TP levels for profit taking
            entry = signal['entry_price']
            tp1 = signal['take_profit']
            
            # Use enhanced TP levels if available
            tp2 = signal.get('take_profit_2', tp1)
            tp3 = signal.get('take_profit_3', tp1)
            
            # If enhanced TPs not available, calculate conservative levels
            if tp2 == tp1:
                if signal['direction'] == 'BUY':
                    tp2 = entry + (reward * 1.5)  # 1.5x reward
                    tp3 = entry + (reward * 2.0)  # 2x reward
                else:
                    tp2 = entry - (reward * 1.5)  # 1.5x reward  
                    tp3 = entry - (reward * 2.0)  # 2x reward
            
            # Risk assessment
            risk_pips = abs(risk * 10000) if 'USD' in signal['symbol'] else abs(risk)
            risk_level = "LOW" if risk_pips < 20 else "MEDIUM" if risk_pips < 35 else "HIGH"
            
            message = f"🎯 <b>{signal['asset_name']}</b> {direction_emoji} {asset_emoji}\n\n"
            message += f"<b>Entry:</b> {signal['entry_price']}\n"
            message += f"<b>SL:</b> {signal['stop_loss']}\n"
            message += f"<b>TP1:</b> {tp1:.5f} (1:{rr_ratio:.1f})\n"
            message += f"<b>TP2:</b> {tp2:.5f} (1:{rr_ratio*1.5:.1f})\n"
            message += f"<b>TP3:</b> {tp3:.5f} (1:{rr_ratio*2:.1f})\n\n"
            # Use calculated position size if available
            position_size = signal.get('position_size', 0.1)
            message += f"📊 <b>Lot Size:</b> {position_size} (optimal) | 0.01 (safe)\n"
            message += f"⚠️ <b>Risk:</b> {risk_level} | {signal.get('confidence', 0):.0%} confidence\n"
            message += f"⏰ <b>Time:</b> {signal['timestamp'].strftime('%H:%M UTC')}"
            
            return message
            
        except Exception as e:
            logger.error(f"Error formatting signal message: {e}")
            return f"Error formatting signal for {signal.get('symbol', 'Unknown')}"
    
    def get_asset_emoji(self, symbol):
        """Get emoji for asset"""
        emoji_map = {
            'EURUSD=X': '🇪🇺🇺🇸',
            'GBPUSD=X': '🇬🇧🇺🇸',
            'XAUUSD=X': '🥇',
            'BTC-USD': '₿'
        }
        return emoji_map.get(symbol, '📊')
    
    def send_signal(self, signal):
        """Send trading signal to Telegram"""
        try:
            message = self.format_signal_message(signal)
            success = self.send_message(message)
            
            if success:
                logger.info(f"Trading signal sent for {signal['symbol']}")
            else:
                logger.error(f"Failed to send trading signal for {signal['symbol']}")
            
            return success
            
        except Exception as e:
            logger.error(f"Error sending signal: {e}")
            return False
    
    def send_error_notification(self, error_message):
        """Send error notification to Telegram"""
        try:
            message = f"🚨 <b>MercuryFX V2 Error</b>\n\n"
            message += f"<b>Error:</b> {error_message}\n"
            message += f"<b>Time:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}\n\n"
            message += f"<i>Please check the bot logs for more details.</i>"
            
            return self.send_message(message)
            
        except Exception as e:
            logger.error(f"Error sending error notification: {e}")
            return False
    
    def send_status_update(self, status_info):
        """Send status update to Telegram"""
        try:
            message = f"📊 <b>MercuryFX V2 Status Update</b>\n\n"
            message += f"<b>Status:</b> {status_info.get('status', 'Running')}\n"
            message += f"<b>Uptime:</b> {status_info.get('uptime', 'Unknown')}\n"
            message += f"<b>Signals Today:</b> {status_info.get('signals_today', 0)}\n"
            message += f"<b>Last Update:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}"
            
            return self.send_message(message)
            
        except Exception as e:
            logger.error(f"Error sending status update: {e}")
            return False
