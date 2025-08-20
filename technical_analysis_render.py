import logging
import math

logger = logging.getLogger(__name__)

class TechnicalAnalysisRender:
    def __init__(self):
        """Initialize technical analysis module with pure Python calculations"""
        logger.info("TechnicalAnalysisRender module initialized")
    
    def calculate_ema(self, prices, period):
        """Calculate Exponential Moving Average"""
        if len(prices) < period:
            return None
            
        alpha = 2 / (period + 1)
        ema = [prices[0]]
        
        for i in range(1, len(prices)):
            ema.append(alpha * prices[i] + (1 - alpha) * ema[i-1])
        
        return ema
    
    def calculate_rsi(self, prices, period=14):
        """Calculate RSI"""
        if len(prices) < period + 1:
            return None
            
        deltas = [prices[i] - prices[i-1] for i in range(1, len(prices))]
        
        gains = [delta if delta > 0 else 0 for delta in deltas]
        losses = [-delta if delta < 0 else 0 for delta in deltas]
        
        # Calculate initial averages
        avg_gain = sum(gains[:period]) / period
        avg_loss = sum(losses[:period]) / period
        
        rsi_values = []
        
        for i in range(period, len(deltas)):
            if avg_loss == 0:
                rsi_values.append(100)
            else:
                rs = avg_gain / avg_loss
                rsi = 100 - (100 / (1 + rs))
                rsi_values.append(rsi)
            
            # Update averages for next iteration
            if i < len(deltas) - 1:
                avg_gain = (avg_gain * (period - 1) + gains[i]) / period
                avg_loss = (avg_loss * (period - 1) + losses[i]) / period
        
        return rsi_values
    
    def calculate_macd(self, prices, fast=12, slow=26, signal=9):
        """Calculate MACD"""
        if len(prices) < slow:
            return None, None, None
            
        ema_fast = self.calculate_ema(prices, fast)
        ema_slow = self.calculate_ema(prices, slow)
        
        if not ema_fast or not ema_slow:
            return None, None, None
        
        # Calculate MACD line
        macd_line = []
        for i in range(len(ema_slow)):
            if i < len(ema_fast):
                macd_line.append(ema_fast[i] - ema_slow[i])
        
        # Calculate signal line
        macd_signal = self.calculate_ema(macd_line, signal)
        
        if not macd_signal:
            return macd_line, None, None
        
        # Calculate histogram
        macd_histogram = []
        for i in range(len(macd_signal)):
            if i < len(macd_line):
                macd_histogram.append(macd_line[i] - macd_signal[i])
        
        return macd_line, macd_signal, macd_histogram
    
    def calculate_indicators(self, market_data):
        """Calculate all technical indicators from market data"""
        try:
            if not market_data or len(market_data['close']) < 200:
                logger.warning("Insufficient data for technical analysis")
                return None
            
            prices = market_data['close']
            
            # Calculate EMAs
            ema50 = self.calculate_ema(prices, 50)
            ema200 = self.calculate_ema(prices, 200)
            
            if not ema50 or not ema200:
                logger.error("Failed to calculate EMAs")
                return None
            
            # Calculate RSI
            rsi = self.calculate_rsi(prices, 14)
            
            if not rsi:
                logger.error("Failed to calculate RSI")
                return None
            
            # Calculate MACD
            macd_line, macd_signal, macd_histogram = self.calculate_macd(prices)
            
            if not macd_line or not macd_signal:
                logger.error("Failed to calculate MACD")
                return None
            
            # Get latest values
            latest_price = prices[-1]
            latest_ema50 = ema50[-1] if ema50 else None
            latest_ema200 = ema200[-1] if ema200 else None
            latest_rsi = rsi[-1] if rsi else None
            latest_macd = macd_line[-1] if macd_line else None
            latest_macd_signal = macd_signal[-1] if macd_signal else None
            latest_macd_histogram = macd_histogram[-1] if macd_histogram else None
            
            indicators = {
                'price': latest_price,
                'ema50': latest_ema50,
                'ema200': latest_ema200,
                'rsi': latest_rsi,
                'macd': latest_macd,
                'macd_signal': latest_macd_signal,
                'macd_histogram': latest_macd_histogram,
                'raw_data': {
                    'prices': prices,
                    'ema50_series': ema50,
                    'ema200_series': ema200,
                    'rsi_series': rsi,
                    'macd_series': macd_line
                }
            }
            
            logger.info(f"Calculated indicators: EMA50={latest_ema50:.5f}, EMA200={latest_ema200:.5f}, RSI={latest_rsi:.2f}")
            return indicators
            
        except Exception as e:
            logger.error(f"Error calculating technical indicators: {e}")
            return None
    
    def get_trend_direction(self, indicators):
        """Determine trend direction from indicators"""
        try:
            ema50 = indicators['ema50']
            ema200 = indicators['ema200']
            rsi = indicators['rsi']
            macd_histogram = indicators['macd_histogram']
            
            # EMA trend
            ema_bullish = ema50 > ema200
            
            # RSI momentum
            rsi_bullish = rsi > 50
            rsi_oversold = rsi < 35
            rsi_overbought = rsi > 65
            
            # MACD momentum
            macd_bullish = macd_histogram > 0
            
            # Combine signals
            bullish_signals = sum([ema_bullish, rsi_bullish, macd_bullish])
            
            if bullish_signals >= 2 and not rsi_overbought:
                return 'BULLISH'
            elif bullish_signals <= 1 and not rsi_oversold:
                return 'BEARISH'
            else:
                return 'NEUTRAL'
                
        except Exception as e:
            logger.error(f"Error determining trend: {e}")
            return 'NEUTRAL'