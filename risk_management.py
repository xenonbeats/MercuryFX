"""
Advanced Risk Management Module for MercuryFX V2
Calculates optimal stop loss and take profit levels using market structure and volatility
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class RiskManager:
    def __init__(self):
        """Initialize advanced risk management system"""
        logger.info("Advanced Risk Management system initialized")
    
    def calculate_atr_volatility(self, data, period=14):
        """Calculate Average True Range for volatility measurement"""
        try:
            high = data['High']
            low = data['Low']
            close = data['Close']
            
            # Calculate True Range components
            tr1 = high - low
            tr2 = abs(high - close.shift(1))
            tr3 = abs(low - close.shift(1))
            
            # True Range is the maximum of the three
            true_range = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
            
            # Average True Range
            atr = true_range.rolling(window=period).mean()
            
            return atr[~pd.isna(atr)]
            
        except Exception as e:
            logger.error(f"Error calculating ATR: {e}")
            return None
    
    def identify_support_resistance(self, data, lookback=20):
        """Identify key support and resistance levels using swing points"""
        try:
            highs = data['High']
            lows = data['Low']
            
            # Find swing highs (resistance)
            resistance_levels = []
            for i in range(lookback, len(highs) - lookback):
                if highs.iloc[i] == highs.iloc[i-lookback:i+lookback+1].max():
                    resistance_levels.append(highs.iloc[i])
            
            # Find swing lows (support)
            support_levels = []
            for i in range(lookback, len(lows) - lookback):
                if lows.iloc[i] == lows.iloc[i-lookback:i+lookback+1].min():
                    support_levels.append(lows.iloc[i])
            
            # Get recent levels (last 10)
            recent_resistance = sorted(resistance_levels[-10:], reverse=True) if resistance_levels else []
            recent_support = sorted(support_levels[-10:]) if support_levels else []
            
            return {
                'resistance': recent_resistance,
                'support': recent_support
            }
            
        except Exception as e:
            logger.error(f"Error identifying support/resistance: {e}")
            return {'resistance': [], 'support': []}
    
    def calculate_optimal_stop_loss(self, entry_price, direction, data, atr):
        """Calculate optimal stop loss based on market structure and volatility"""
        try:
            current_atr = atr.iloc[-1]
            
            # Get support/resistance levels
            levels = self.identify_support_resistance(data)
            
            if direction == 'BUY':
                # For BUY orders, SL should be below recent support
                base_sl = entry_price - (current_atr * 1.5)  # 1.5x ATR below entry
                
                # Find nearest support level below entry
                support_below = [level for level in levels['support'] if level < entry_price]
                if support_below:
                    nearest_support = max(support_below)
                    # Place SL slightly below nearest support
                    structure_sl = nearest_support - (current_atr * 0.3)
                    
                    # Use the more conservative (closer to entry) SL
                    optimal_sl = max(base_sl, structure_sl)
                else:
                    optimal_sl = base_sl
                    
            else:  # SELL
                # For SELL orders, SL should be above recent resistance
                base_sl = entry_price + (current_atr * 1.5)  # 1.5x ATR above entry
                
                # Find nearest resistance level above entry
                resistance_above = [level for level in levels['resistance'] if level > entry_price]
                if resistance_above:
                    nearest_resistance = min(resistance_above)
                    # Place SL slightly above nearest resistance
                    structure_sl = nearest_resistance + (current_atr * 0.3)
                    
                    # Use the more conservative (closer to entry) SL
                    optimal_sl = min(base_sl, structure_sl)
                else:
                    optimal_sl = base_sl
            
            return optimal_sl
            
        except Exception as e:
            logger.error(f"Error calculating optimal stop loss: {e}")
            # Fallback to simple ATR-based SL
            return entry_price - (atr.iloc[-1] * 1.5) if direction == 'BUY' else entry_price + (atr.iloc[-1] * 1.5)
    
    def calculate_optimal_take_profit(self, entry_price, stop_loss, direction, data, atr, target_rr=2.5):
        """Calculate optimal take profit with multiple levels"""
        try:
            current_atr = atr.iloc[-1]
            
            # Calculate risk (distance from entry to SL)
            risk = abs(entry_price - stop_loss)
            
            # Get support/resistance levels for target placement
            levels = self.identify_support_resistance(data)
            
            if direction == 'BUY':
                # Base TP using risk/reward ratio
                base_tp1 = entry_price + (risk * target_rr)
                
                # Find resistance levels above entry for realistic targets
                resistance_above = [level for level in levels['resistance'] if level > entry_price]
                
                if resistance_above:
                    # Adjust TP to respect resistance levels
                    nearest_resistance = min(resistance_above)
                    if base_tp1 > nearest_resistance:
                        # Place TP slightly before resistance
                        tp1 = nearest_resistance - (current_atr * 0.2)
                    else:
                        tp1 = base_tp1
                else:
                    tp1 = base_tp1
                    
                # Additional TP levels
                tp2 = entry_price + (risk * (target_rr + 1.0))  # Higher R:R
                tp3 = entry_price + (risk * (target_rr + 2.0))  # Extended target
                
            else:  # SELL
                # Base TP using risk/reward ratio
                base_tp1 = entry_price - (risk * target_rr)
                
                # Find support levels below entry for realistic targets
                support_below = [level for level in levels['support'] if level < entry_price]
                
                if support_below:
                    # Adjust TP to respect support levels
                    nearest_support = max(support_below)
                    if base_tp1 < nearest_support:
                        # Place TP slightly before support
                        tp1 = nearest_support + (current_atr * 0.2)
                    else:
                        tp1 = base_tp1
                else:
                    tp1 = base_tp1
                    
                # Additional TP levels
                tp2 = entry_price - (risk * (target_rr + 1.0))  # Higher R:R
                tp3 = entry_price - (risk * (target_rr + 2.0))  # Extended target
            
            return {
                'tp1': tp1,
                'tp2': tp2,
                'tp3': tp3,
                'risk_amount': risk,
                'rr_ratio': abs(tp1 - entry_price) / risk
            }
            
        except Exception as e:
            logger.error(f"Error calculating optimal take profit: {e}")
            # Fallback calculation
            risk = abs(entry_price - stop_loss)
            tp1 = entry_price + (risk * target_rr) if direction == 'BUY' else entry_price - (risk * target_rr)
            return {
                'tp1': tp1,
                'tp2': tp1,
                'tp3': tp1,
                'risk_amount': risk,
                'rr_ratio': target_rr
            }
    
    def validate_trade_risk(self, entry_price, stop_loss, take_profit, symbol):
        """Validate if trade risk is acceptable"""
        try:
            risk = abs(entry_price - stop_loss)
            reward = abs(take_profit - entry_price)
            rr_ratio = reward / risk if risk > 0 else 0
            
            # Risk validation rules
            if 'USD' in symbol:
                # Forex pairs - risk in pips
                risk_pips = risk * 10000
                
                # Minimum R:R ratio
                if rr_ratio < 1.8:
                    return False, f"R:R ratio too low: {rr_ratio:.1f}"
                
                # Maximum risk per trade (in pips)
                if risk_pips > 40:
                    return False, f"Risk too high: {risk_pips:.1f} pips"
                
                # Minimum risk (avoid over-tight stops)
                if risk_pips < 8:
                    return False, f"Stop too tight: {risk_pips:.1f} pips"
                    
            else:
                # Crypto/commodities
                risk_percent = (risk / entry_price) * 100
                
                if rr_ratio < 1.8:
                    return False, f"R:R ratio too low: {rr_ratio:.1f}"
                
                if risk_percent > 2.5:
                    return False, f"Risk too high: {risk_percent:.1f}%"
                    
                if risk_percent < 0.3:
                    return False, f"Stop too tight: {risk_percent:.1f}%"
            
            return True, f"Risk validated: {rr_ratio:.1f} R:R"
            
        except Exception as e:
            logger.error(f"Error validating trade risk: {e}")
            return False, "Risk validation failed"
    
    def calculate_position_size(self, account_balance, risk_percent, entry_price, stop_loss, symbol):
        """Calculate optimal position size based on risk management"""
        try:
            # Risk amount in account currency
            risk_amount = account_balance * (risk_percent / 100)
            
            # Risk per unit
            risk_per_unit = abs(entry_price - stop_loss)
            
            if 'USD' in symbol:
                # Forex - standard lot calculation
                pip_value = 10  # $10 per pip for standard lot
                risk_pips = risk_per_unit * 10000
                max_lots = risk_amount / (risk_pips * pip_value)
                
                # Round to appropriate lot sizes
                if max_lots >= 1.0:
                    lot_size = round(max_lots, 1)
                elif max_lots >= 0.1:
                    lot_size = round(max_lots, 2)
                else:
                    lot_size = 0.01  # Minimum lot
                    
            else:
                # Crypto/commodities - unit calculation
                max_units = risk_amount / risk_per_unit
                lot_size = round(max_units, 4)
            
            return max(lot_size, 0.01)  # Minimum 0.01 lot
            
        except Exception as e:
            logger.error(f"Error calculating position size: {e}")
            return 0.01  # Safe minimum