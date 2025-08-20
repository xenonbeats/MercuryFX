import logging
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

class SmartMoneyConcepts:
    """
    Advanced Smart Money Concepts (SMC) analysis including:
    - Break of Structure (BOS)
    - Market Structure Shift (MSS) 
    - Fair Value Gap (FVG)
    - Order Block detection
    - Liquidity analysis
    """
    
    def __init__(self):
        self.swing_strength = 5  # Number of bars to look back/forward for swing highs/lows
        self.fvg_threshold = 0.0001  # Minimum gap size for FVG (adjustable per asset)
        logger.info("Smart Money Concepts module initialized")
    
    def identify_swing_points(self, data: pd.DataFrame) -> Dict:
        """Identify swing highs and lows in the data"""
        try:
            df = data.copy()
            swing_highs = []
            swing_lows = []
            
            high_col = df['High'].values
            low_col = df['Low'].values
            
            for i in range(self.swing_strength, len(df) - self.swing_strength):
                # Check for swing high
                is_swing_high = True
                for j in range(i - self.swing_strength, i + self.swing_strength + 1):
                    if j != i and high_col[j] >= high_col[i]:
                        is_swing_high = False
                        break
                
                if is_swing_high:
                    swing_highs.append({
                        'index': i,
                        'timestamp': df.index[i],
                        'price': high_col[i],
                        'type': 'swing_high'
                    })
                
                # Check for swing low
                is_swing_low = True
                for j in range(i - self.swing_strength, i + self.swing_strength + 1):
                    if j != i and low_col[j] <= low_col[i]:
                        is_swing_low = False
                        break
                
                if is_swing_low:
                    swing_lows.append({
                        'index': i,
                        'timestamp': df.index[i],
                        'price': low_col[i],
                        'type': 'swing_low'
                    })
            
            return {
                'swing_highs': swing_highs,
                'swing_lows': swing_lows
            }
            
        except Exception as e:
            logger.error(f"Error identifying swing points: {e}")
            return {'swing_highs': [], 'swing_lows': []}
    
    def detect_break_of_structure(self, data: pd.DataFrame, swing_points: Dict) -> Dict:
        """Detect Break of Structure (BOS) - continuation pattern"""
        try:
            bos_signals = []
            swing_highs = swing_points['swing_highs']
            swing_lows = swing_points['swing_lows']
            
            current_price = data['Close'].iloc[-1]
            
            # Check for bullish BOS (breaking previous swing high)
            if len(swing_highs) >= 2:
                latest_high = swing_highs[-1]
                if current_price > latest_high['price']:
                    bos_signals.append({
                        'type': 'BOS_BULLISH',
                        'direction': 'BUY',
                        'strength': 'HIGH',
                        'price': current_price,
                        'broken_level': latest_high['price'],
                        'confidence': 0.8
                    })
            
            # Check for bearish BOS (breaking previous swing low)
            if len(swing_lows) >= 2:
                latest_low = swing_lows[-1]
                if current_price < latest_low['price']:
                    bos_signals.append({
                        'type': 'BOS_BEARISH',
                        'direction': 'SELL',
                        'strength': 'HIGH',
                        'price': current_price,
                        'broken_level': latest_low['price'],
                        'confidence': 0.8
                    })
            
            return {'bos_signals': bos_signals}
            
        except Exception as e:
            logger.error(f"Error detecting BOS: {e}")
            return {'bos_signals': []}
    
    def detect_market_structure_shift(self, data: pd.DataFrame, swing_points: Dict) -> Dict:
        """Detect Market Structure Shift (MSS) - reversal pattern"""
        try:
            mss_signals = []
            swing_highs = swing_points['swing_highs']
            swing_lows = swing_points['swing_lows']
            
            current_price = data['Close'].iloc[-1]
            
            # Check for bearish MSS (in uptrend, price breaks previous swing low)
            if len(swing_lows) >= 2 and len(swing_highs) >= 1:
                recent_low = swing_lows[-1]
                recent_high = swing_highs[-1]
                
                # Ensure we were in an uptrend
                if recent_high['timestamp'] > recent_low['timestamp']:
                    if current_price < recent_low['price']:
                        mss_signals.append({
                            'type': 'MSS_BEARISH',
                            'direction': 'SELL',
                            'strength': 'VERY_HIGH',
                            'price': current_price,
                            'broken_level': recent_low['price'],
                            'confidence': 0.85
                        })
            
            # Check for bullish MSS (in downtrend, price breaks previous swing high)
            if len(swing_highs) >= 2 and len(swing_lows) >= 1:
                recent_high = swing_highs[-1]
                recent_low = swing_lows[-1]
                
                # Ensure we were in a downtrend
                if recent_low['timestamp'] > recent_high['timestamp']:
                    if current_price > recent_high['price']:
                        mss_signals.append({
                            'type': 'MSS_BULLISH',
                            'direction': 'BUY',
                            'strength': 'VERY_HIGH',
                            'price': current_price,
                            'broken_level': recent_high['price'],
                            'confidence': 0.85
                        })
            
            return {'mss_signals': mss_signals}
            
        except Exception as e:
            logger.error(f"Error detecting MSS: {e}")
            return {'mss_signals': []}
    
    def detect_fair_value_gaps(self, data: pd.DataFrame) -> Dict:
        """Detect Fair Value Gaps (FVG) - imbalance in price action"""
        try:
            fvg_signals = []
            df = data.copy()
            
            for i in range(2, len(df)):
                # Bullish FVG: Gap between candle 1 high and candle 3 low
                candle1_high = df['High'].iloc[i-2]
                candle2_low = df['Low'].iloc[i-1]
                candle2_high = df['High'].iloc[i-1]
                candle3_low = df['Low'].iloc[i]
                
                # Bullish FVG condition
                if candle1_high < candle3_low:
                    gap_size = candle3_low - candle1_high
                    if gap_size > self.fvg_threshold:
                        fvg_signals.append({
                            'type': 'FVG_BULLISH',
                            'direction': 'BUY',
                            'strength': 'MEDIUM',
                            'gap_top': candle3_low,
                            'gap_bottom': candle1_high,
                            'gap_size': gap_size,
                            'index': i,
                            'confidence': 0.7
                        })
                
                # Bearish FVG: Gap between candle 1 low and candle 3 high
                candle1_low = df['Low'].iloc[i-2]
                candle3_high = df['High'].iloc[i]
                
                # Bearish FVG condition
                if candle1_low > candle3_high:
                    gap_size = candle1_low - candle3_high
                    if gap_size > self.fvg_threshold:
                        fvg_signals.append({
                            'type': 'FVG_BEARISH',
                            'direction': 'SELL',
                            'strength': 'MEDIUM',
                            'gap_top': candle1_low,
                            'gap_bottom': candle3_high,
                            'gap_size': gap_size,
                            'index': i,
                            'confidence': 0.7
                        })
            
            return {'fvg_signals': fvg_signals[-5:]}  # Return last 5 FVGs
            
        except Exception as e:
            logger.error(f"Error detecting FVG: {e}")
            return {'fvg_signals': []}
    
    def detect_order_blocks(self, data: pd.DataFrame, swing_points: Dict) -> Dict:
        """Detect Order Blocks - institutional supply/demand zones"""
        try:
            order_blocks = []
            swing_highs = swing_points['swing_highs']
            swing_lows = swing_points['swing_lows']
            
            # Bullish Order Block: Last down candle before swing low
            for swing_low in swing_lows[-3:]:  # Check last 3 swing lows
                swing_idx = swing_low['index']
                if swing_idx > 0:
                    # Look for the last bearish candle before the swing low
                    for j in range(swing_idx - 1, max(0, swing_idx - 10), -1):
                        if data['Close'].iloc[j] < data['Open'].iloc[j]:  # Bearish candle
                            order_blocks.append({
                                'type': 'ORDER_BLOCK_BULLISH',
                                'direction': 'BUY',
                                'strength': 'HIGH',
                                'zone_top': data['High'].iloc[j],
                                'zone_bottom': data['Low'].iloc[j],
                                'index': j,
                                'confidence': 0.75
                            })
                            break
            
            # Bearish Order Block: Last up candle before swing high
            for swing_high in swing_highs[-3:]:  # Check last 3 swing highs
                swing_idx = swing_high['index']
                if swing_idx > 0:
                    # Look for the last bullish candle before the swing high
                    for j in range(swing_idx - 1, max(0, swing_idx - 10), -1):
                        if data['Close'].iloc[j] > data['Open'].iloc[j]:  # Bullish candle
                            order_blocks.append({
                                'type': 'ORDER_BLOCK_BEARISH',
                                'direction': 'SELL',
                                'strength': 'HIGH',
                                'zone_top': data['High'].iloc[j],
                                'zone_bottom': data['Low'].iloc[j],
                                'index': j,
                                'confidence': 0.75
                            })
                            break
            
            return {'order_blocks': order_blocks}
            
        except Exception as e:
            logger.error(f"Error detecting order blocks: {e}")
            return {'order_blocks': []}
    
    def analyze_smart_money_concepts(self, data: pd.DataFrame, symbol: str) -> Dict:
        """Complete SMC analysis combining all concepts"""
        try:
            # Adjust FVG threshold based on asset type
            if 'USD' in symbol and '=' in symbol:  # Forex pairs
                self.fvg_threshold = 0.0001
            elif 'XAU' in symbol:  # Gold
                self.fvg_threshold = 0.5
            else:  # Crypto
                self.fvg_threshold = 5.0
            
            # Get swing points
            swing_points = self.identify_swing_points(data)
            
            # Detect all patterns
            bos_analysis = self.detect_break_of_structure(data, swing_points)
            mss_analysis = self.detect_market_structure_shift(data, swing_points)
            fvg_analysis = self.detect_fair_value_gaps(data)
            order_block_analysis = self.detect_order_blocks(data, swing_points)
            
            # Combine all analyses
            smc_analysis = {
                'swing_points': swing_points,
                'bos': bos_analysis,
                'mss': mss_analysis,
                'fvg': fvg_analysis,
                'order_blocks': order_block_analysis,
                'timestamp': data.index[-1],
                'current_price': data['Close'].iloc[-1]
            }
            
            logger.debug(f"SMC analysis completed for {symbol}")
            return smc_analysis
            
        except Exception as e:
            logger.error(f"Error in SMC analysis for {symbol}: {e}")
            return {}
    
    def calculate_smc_signal_strength(self, smc_analysis: Dict) -> Dict:
        """Calculate overall signal strength based on SMC confluence"""
        try:
            signals = []
            total_confidence = 0
            signal_count = 0
            
            # Check BOS signals
            for signal in smc_analysis.get('bos', {}).get('bos_signals', []):
                signals.append(signal)
                total_confidence += signal['confidence']
                signal_count += 1
            
            # Check MSS signals (higher priority)
            for signal in smc_analysis.get('mss', {}).get('mss_signals', []):
                signals.append(signal)
                total_confidence += signal['confidence'] * 1.2  # MSS gets higher weight
                signal_count += 1
            
            # Check FVG signals
            for signal in smc_analysis.get('fvg', {}).get('fvg_signals', []):
                if len(signals) > 0 and signals[-1]['direction'] == signal['direction']:
                    # FVG confirms other signals
                    total_confidence += signal['confidence'] * 0.8
                    signal_count += 1
            
            # Check Order Block signals
            for signal in smc_analysis.get('order_blocks', {}).get('order_blocks', []):
                if len(signals) > 0 and signals[-1]['direction'] == signal['direction']:
                    # Order block confirms other signals
                    total_confidence += signal['confidence'] * 0.9
                    signal_count += 1
            
            if signal_count == 0:
                return {'action': 'HOLD', 'confidence': 0, 'signals': []}
            
            avg_confidence = total_confidence / signal_count
            
            # Determine primary direction
            buy_signals = [s for s in signals if s['direction'] == 'BUY']
            sell_signals = [s for s in signals if s['direction'] == 'SELL']
            
            if len(buy_signals) > len(sell_signals) and avg_confidence > 0.7:
                primary_direction = 'BUY'
            elif len(sell_signals) > len(buy_signals) and avg_confidence > 0.7:
                primary_direction = 'SELL'
            else:
                primary_direction = 'HOLD'
            
            return {
                'action': primary_direction,
                'confidence': min(avg_confidence, 1.0),
                'signal_count': signal_count,
                'signals': signals,
                'risk_quality': 'HIGH' if avg_confidence > 0.8 else 'MEDIUM' if avg_confidence > 0.6 else 'LOW'
            }
            
        except Exception as e:
            logger.error(f"Error calculating SMC signal strength: {e}")
            return {'action': 'HOLD', 'confidence': 0, 'signals': []}