import logging
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)

class TechnicalAnalysis:
    def __init__(self):
        """Initialize technical analysis module"""
        logger.info("TechnicalAnalysis module initialized")
    
    def calculate_ema(self, data, period):
        """Calculate Exponential Moving Average manually"""
        alpha = 2 / (period + 1)
        ema = [data.iloc[0]]
        
        for i in range(1, len(data)):
            ema.append(alpha * data.iloc[i] + (1 - alpha) * ema[i-1])
        
        return pd.Series(ema, index=data.index)
    
    def calculate_rsi(self, data, period=14):
        """Calculate RSI manually"""
        delta = data.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def calculate_macd(self, data, fast=12, slow=26, signal=9):
        """Calculate MACD manually"""
        ema_fast = self.calculate_ema(data, fast)
        ema_slow = self.calculate_ema(data, slow)
        macd_line = ema_fast - ema_slow
        macd_signal = self.calculate_ema(macd_line, signal)
        macd_histogram = macd_line - macd_signal
        return macd_line, macd_signal, macd_histogram
    
    def calculate_indicators(self, data):
        """Calculate all required technical indicators using pure Python"""
        try:
            if len(data) < 200:  # Need enough data for EMA200
                logger.warning("Insufficient data for technical analysis")
                return None
            
            # Create a copy to avoid modifying original data
            df = data.copy()
            
            # Calculate EMAs manually
            df['ema50'] = self.calculate_ema(df['Close'], 50)
            df['ema200'] = self.calculate_ema(df['Close'], 200)
            
            # Calculate RSI manually
            df['rsi'] = self.calculate_rsi(df['Close'], 14)
            
            # Calculate MACD manually
            macd_line, macd_signal, macd_histogram = self.calculate_macd(df['Close'])
            df['macd'] = macd_line
            df['macd_signal'] = macd_signal
            df['macd_histogram'] = macd_histogram
            
            # Remove NaN values
            df = df.dropna()
            
            if len(df) == 0:
                logger.warning("No valid data after indicator calculation")
                return None
            
            indicators = {
                'ema50': df['ema50'],
                'ema200': df['ema200'],
                'rsi': df['rsi'],
                'macd': df['macd'],
                'macd_signal': df['macd_signal'],
                'macd_histogram': df['macd_histogram']
            }
            
            logger.debug(f"Calculated indicators for {len(df)} data points")
            return indicators
            
        except Exception as e:
            logger.error(f"Error calculating indicators: {e}")
            return None
    
    def get_trend_direction(self, indicators):
        """Determine overall trend direction"""
        try:
            if not indicators:
                return "NEUTRAL"
            
            latest_ema50 = indicators['ema50'].iloc[-1]
            latest_ema200 = indicators['ema200'].iloc[-1]
            latest_rsi = indicators['rsi'].iloc[-1]
            latest_macd = indicators['macd'].iloc[-1]
            
            bullish_signals = 0
            bearish_signals = 0
            
            # EMA trend
            if latest_ema50 > latest_ema200:
                bullish_signals += 1
            else:
                bearish_signals += 1
            
            # RSI trend
            if latest_rsi > 50:
                bullish_signals += 1
            else:
                bearish_signals += 1
            
            # MACD trend
            if latest_macd > 0:
                bullish_signals += 1
            else:
                bearish_signals += 1
            
            if bullish_signals > bearish_signals:
                return "BULLISH"
            elif bearish_signals > bullish_signals:
                return "BEARISH"
            else:
                return "NEUTRAL"
                
        except Exception as e:
            logger.error(f"Error determining trend direction: {e}")
            return "NEUTRAL"
    
    def format_indicator_summary(self, indicators):
        """Format indicators for display"""
        try:
            if not indicators:
                return "No indicator data available"
            
            latest_ema50 = indicators['ema50'].iloc[-1]
            latest_ema200 = indicators['ema200'].iloc[-1]
            latest_rsi = indicators['rsi'].iloc[-1]
            latest_macd = indicators['macd'].iloc[-1]
            
            summary = f"EMA50: {latest_ema50:.5f}\n"
            summary += f"EMA200: {latest_ema200:.5f}\n"
            summary += f"RSI(14): {latest_rsi:.2f}\n"
            summary += f"MACD: {latest_macd:.5f}"
            
            return summary
            
        except Exception as e:
            logger.error(f"Error formatting indicator summary: {e}")
            return "Error formatting indicators"
