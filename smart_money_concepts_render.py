import logging
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

class SmartMoneyConceptsRender:
    """
    Smart Money Concepts (SMC) analysis adapted for pure Python:
    - Break of Structure (BOS)
    - Market Structure Shift (MSS) 
    - Fair Value Gap (FVG)
    - Order Block detection
    - Simplified for Render deployment
    """
    
    def __init__(self):
        self.swing_strength = 5
        self.fvg_threshold = 0.0001
        logger.info("Smart Money Concepts Render module initialized")
    
    def identify_swing_points(self, market_data: Dict) -> Dict:
        """Identify swing highs and lows"""
        try:
            highs = market_data['high']
            lows = market_data['low']
            timestamps = market_data['timestamps']
            
            swing_highs = []
            swing_lows = []
            
            for i in range(self.swing_strength, len(highs) - self.swing_strength):
                # Check for swing high
                is_swing_high = True
                for j in range(i - self.swing_strength, i + self.swing_strength + 1):
                    if j != i and highs[j] >= highs[i]:
                        is_swing_high = False
                        break
                
                if is_swing_high:
                    swing_highs.append({
                        'index': i,
                        'timestamp': timestamps[i],
                        'price': highs[i],
                        'type': 'swing_high'
                    })
                
                # Check for swing low
                is_swing_low = True
                for j in range(i - self.swing_strength, i + self.swing_strength + 1):
                    if j != i and lows[j] <= lows[i]:
                        is_swing_low = False
                        break
                
                if is_swing_low:
                    swing_lows.append({
                        'index': i,
                        'timestamp': timestamps[i],
                        'price': lows[i],
                        'type': 'swing_low'
                    })
            
            return {
                'swing_highs': swing_highs,
                'swing_lows': swing_lows
            }
            
        except Exception as e:
            logger.error(f"Error identifying swing points: {e}")
            return {'swing_highs': [], 'swing_lows': []}
    
    def detect_break_of_structure(self, market_data: Dict, swing_points: Dict) -> Dict:
        """Detect Break of Structure (BOS) - continuation pattern"""
        try:
            bos_signals = []
            swing_highs = swing_points['swing_highs']
            swing_lows = swing_points['swing_lows']
            current_price = market_data['close'][-1]
            
            # Check for bullish BOS (breaking recent swing high)
            if len(swing_highs) >= 2:
                recent_high = swing_highs[-1]
                if current_price > recent_high['price']:
                    bos_signals.append({
                        'type': 'BOS_BULLISH',
                        'broken_level': recent_high['price'],
                        'current_price': current_price,
                        'confidence': 0.7
                    })
            
            # Check for bearish BOS (breaking recent swing low)
            if len(swing_lows) >= 2:
                recent_low = swing_lows[-1]
                if current_price < recent_low['price']:
                    bos_signals.append({
                        'type': 'BOS_BEARISH',
                        'broken_level': recent_low['price'],
                        'current_price': current_price,
                        'confidence': 0.7
                    })
            
            return {'bos_signals': bos_signals}
            
        except Exception as e:
            logger.error(f"Error detecting BOS: {e}")
            return {'bos_signals': []}
    
    def detect_market_structure_shift(self, market_data: Dict, swing_points: Dict) -> Dict:
        """Detect Market Structure Shift (MSS) - reversal pattern"""
        try:
            mss_signals = []
            swing_highs = swing_points['swing_highs']
            swing_lows = swing_points['swing_lows']
            current_price = market_data['close'][-1]
            
            # Simplified MSS detection
            if len(swing_highs) >= 2 and len(swing_lows) >= 2:
                latest_high = swing_highs[-1]
                latest_low = swing_lows[-1]
                
                # Check for bearish MSS (break of recent low after making higher high)
                if (latest_high['timestamp'] > latest_low['timestamp'] and 
                    current_price < latest_low['price']):
                    mss_signals.append({
                        'type': 'MSS_BEARISH',
                        'broken_level': latest_low['price'],
                        'current_price': current_price,
                        'confidence': 0.8
                    })
                
                # Check for bullish MSS (break of recent high after making lower low)
                elif (latest_low['timestamp'] > latest_high['timestamp'] and 
                      current_price > latest_high['price']):
                    mss_signals.append({
                        'type': 'MSS_BULLISH',
                        'broken_level': latest_high['price'],
                        'current_price': current_price,
                        'confidence': 0.8
                    })
            
            return {'mss_signals': mss_signals}
            
        except Exception as e:
            logger.error(f"Error detecting MSS: {e}")
            return {'mss_signals': []}
    
    def detect_fair_value_gaps(self, market_data: Dict) -> Dict:
        """Detect Fair Value Gaps (FVG)"""
        try:
            fvg_signals = []
            highs = market_data['high']
            lows = market_data['low']
            opens = market_data['open']
            closes = market_data['close']
            
            for i in range(2, len(highs)):
                # Bullish FVG: current low > previous high (gap up)
                if lows[i] > highs[i-2]:
                    gap_size = lows[i] - highs[i-2]
                    if gap_size > self.fvg_threshold:
                        fvg_signals.append({
                            'type': 'FVG_BULLISH',
                            'gap_low': highs[i-2],
                            'gap_high': lows[i],
                            'gap_size': gap_size,
                            'index': i,
                            'confidence': min(0.9, 0.5 + (gap_size * 1000))
                        })
                
                # Bearish FVG: current high < previous low (gap down)
                elif highs[i] < lows[i-2]:
                    gap_size = lows[i-2] - highs[i]
                    if gap_size > self.fvg_threshold:
                        fvg_signals.append({
                            'type': 'FVG_BEARISH',
                            'gap_low': highs[i],
                            'gap_high': lows[i-2],
                            'gap_size': gap_size,
                            'index': i,
                            'confidence': min(0.9, 0.5 + (gap_size * 1000))
                        })
            
            return {'fvg_signals': fvg_signals}
            
        except Exception as e:
            logger.error(f"Error detecting FVG: {e}")
            return {'fvg_signals': []}
    
    def detect_order_blocks(self, market_data: Dict) -> Dict:
        """Detect Order Blocks"""
        try:
            order_blocks = []
            highs = market_data['high']
            lows = market_data['low']
            closes = market_data['close']
            volumes = market_data['volume']
            
            for i in range(10, len(closes) - 5):
                # Look for significant volume and price movement
                avg_volume = sum(volumes[i-10:i]) / 10 if volumes[i] > 0 else 1
                current_volume = volumes[i] or avg_volume
                
                # Bullish order block (demand zone)
                if (current_volume > avg_volume * 1.5 and
                    closes[i] > closes[i-1] and
                    closes[i+1] > closes[i]):
                    
                    order_blocks.append({
                        'type': 'ORDER_BLOCK_BULLISH',
                        'zone_low': lows[i],
                        'zone_high': highs[i],
                        'volume_confirmation': current_volume > avg_volume * 1.5,
                        'confidence': 0.6
                    })
                
                # Bearish order block (supply zone)
                elif (current_volume > avg_volume * 1.5 and
                      closes[i] < closes[i-1] and
                      closes[i+1] < closes[i]):
                    
                    order_blocks.append({
                        'type': 'ORDER_BLOCK_BEARISH',
                        'zone_low': lows[i],
                        'zone_high': highs[i],
                        'volume_confirmation': current_volume > avg_volume * 1.5,
                        'confidence': 0.6
                    })
            
            return {'order_blocks': order_blocks}
            
        except Exception as e:
            logger.error(f"Error detecting order blocks: {e}")
            return {'order_blocks': []}
    
    def analyze_smart_money_concepts(self, market_data: Dict, symbol: str) -> Optional[Dict]:
        """Main SMC analysis function"""
        try:
            if not market_data or len(market_data['close']) < 50:
                logger.warning(f"Insufficient data for SMC analysis: {symbol}")
                return None
            
            # Identify swing points
            swing_points = self.identify_swing_points(market_data)
            
            # Detect all SMC patterns
            bos_analysis = self.detect_break_of_structure(market_data, swing_points)
            mss_analysis = self.detect_market_structure_shift(market_data, swing_points)
            fvg_analysis = self.detect_fair_value_gaps(market_data)
            order_block_analysis = self.detect_order_blocks(market_data)
            
            # Calculate SMC score
            smc_patterns = (len(bos_analysis['bos_signals']) + 
                          len(mss_analysis['mss_signals']) + 
                          len(fvg_analysis['fvg_signals']) + 
                          len(order_block_analysis['order_blocks']))
            
            smc_confidence = min(0.9, 0.3 + (smc_patterns * 0.15))
            
            smc_data = {
                'swing_points': swing_points,
                'bos_analysis': bos_analysis,
                'mss_analysis': mss_analysis,
                'fvg_analysis': fvg_analysis,
                'order_block_analysis': order_block_analysis,
                'smc_patterns_count': smc_patterns,
                'smc_confidence': smc_confidence,
                'has_smc_confluence': smc_patterns >= 2,
                'analysis_timestamp': market_data['timestamps'][-1] if market_data['timestamps'] else None
            }
            
            logger.info(f"SMC Analysis for {symbol}: {smc_patterns} patterns, confidence: {smc_confidence:.2f}")
            return smc_data
            
        except Exception as e:
            logger.error(f"Error in SMC analysis for {symbol}: {e}")
            return None
    
    def calculate_smc_signal_strength(self, smc_analysis: Dict) -> Dict:
        """Calculate SMC signal strength and direction"""
        try:
            if not smc_analysis:
                return {'direction': 'NEUTRAL', 'strength': 0.0, 'confluence': 0}
            
            bullish_signals = 0
            bearish_signals = 0
            total_confidence = 0.0
            
            # Count BOS signals
            for bos in smc_analysis['bos_analysis']['bos_signals']:
                if bos['type'] == 'BOS_BULLISH':
                    bullish_signals += 1
                    total_confidence += bos['confidence']
                else:
                    bearish_signals += 1
                    total_confidence += bos['confidence']
            
            # Count MSS signals
            for mss in smc_analysis['mss_analysis']['mss_signals']:
                if mss['type'] == 'MSS_BULLISH':
                    bullish_signals += 1
                    total_confidence += mss['confidence']
                else:
                    bearish_signals += 1
                    total_confidence += mss['confidence']
            
            # Count FVG signals
            for fvg in smc_analysis['fvg_analysis']['fvg_signals']:
                if fvg['type'] == 'FVG_BULLISH':
                    bullish_signals += 1
                    total_confidence += fvg['confidence']
                else:
                    bearish_signals += 1
                    total_confidence += fvg['confidence']
            
            # Count Order Block signals
            for ob in smc_analysis['order_block_analysis']['order_blocks']:
                if ob['type'] == 'ORDER_BLOCK_BULLISH':
                    bullish_signals += 1
                    total_confidence += ob['confidence']
                else:
                    bearish_signals += 1
                    total_confidence += ob['confidence']
            
            # Determine direction and strength
            total_signals = bullish_signals + bearish_signals
            if total_signals == 0:
                direction = 'NEUTRAL'
                strength = 0.0
            elif bullish_signals > bearish_signals:
                direction = 'BUY'
                strength = min(0.95, total_confidence / total_signals)
            elif bearish_signals > bullish_signals:
                direction = 'SELL'
                strength = min(0.95, total_confidence / total_signals)
            else:
                direction = 'NEUTRAL'
                strength = total_confidence / total_signals if total_signals > 0 else 0.0
            
            return {
                'direction': direction,
                'strength': strength,
                'confluence': total_signals,
                'bullish_signals': bullish_signals,
                'bearish_signals': bearish_signals
            }
            
        except Exception as e:
            logger.error(f"Error calculating SMC signal strength: {e}")
            return {'direction': 'NEUTRAL', 'strength': 0.0, 'confluence': 0}