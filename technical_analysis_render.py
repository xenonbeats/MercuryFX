import logging
import pandas as pd
import ta

logger = logging.getLogger(__name__)

class TechnicalAnalysis:
    def __init__(self):
        """Initialize technical analysis module"""
        logger.info("TechnicalAnalysis module initialized")
    
    def calculate_indicators(self, data):
        """Calculate all required technical indicators using ta library (Render compatible)"""
        try:
            if len(data) < 200:  # Need enough data for EMA200
                logger.warning("Insufficient data for technical analysis")
                return None
            
            # Create a copy to avoid modifying original data
            df = data.copy()
            
            # Calculate EMAs using ta library
            df['ema50'] = ta.trend.ema_indicator(df['Close'], window=50)
            df['ema200'] = ta.trend.ema_indicator(df['Close'], window=200)
            
            # Calculate RSI using ta library
            df['rsi'] = ta.momentum.rsi(df['Close'], window=14)
            
            # Calculate MACD using ta library
            df['macd'] = ta.trend.macd_diff(df['Close'])
            df['macd_signal'] = ta.trend.macd_signal(df['Close'])
            df['macd_histogram'] = ta.trend.macd(df['Close']) - ta.trend.macd_signal(df['Close'])
            
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
            
            summary = f"EMA50: {latest_ema50:.5f}, EMA200: {latest_ema200:.5f}, "
            summary += f"RSI: {latest_rsi:.1f}, MACD: {latest_macd:.5f}"
            
            return summary
            
        except Exception as e:
            logger.error(f"Error formatting indicators: {e}")
            return "Error formatting indicators"
    
    def get_signal_strength(self, indicators):
        """Calculate signal strength based on indicator alignment"""
        try:
            if not indicators:
                return 0.0
                
            latest_ema50 = indicators['ema50'].iloc[-1]
            latest_ema200 = indicators['ema200'].iloc[-1]
            latest_rsi = indicators['rsi'].iloc[-1]
            latest_macd = indicators['macd'].iloc[-1]
            latest_macd_signal = indicators['macd_signal'].iloc[-1]
            
            strength = 0.0
            max_strength = 5.0
            
            # EMA alignment (20% weight)
            if latest_ema50 > latest_ema200:
                strength += 1.0
            
            # RSI momentum (20% weight)
            if 30 <= latest_rsi <= 70:  # Not oversold/overbought
                strength += 1.0
            
            # MACD signal (20% weight)  
            if latest_macd > latest_macd_signal:
                strength += 1.0
                
            # MACD zero line (20% weight)
            if latest_macd > 0:
                strength += 1.0
                
            # RSI trend strength (20% weight)
            if latest_rsi > 50:
                strength += 1.0
            
            return strength / max_strength
            
        except Exception as e:
            logger.error(f"Error calculating signal strength: {e}")
            return 0.0