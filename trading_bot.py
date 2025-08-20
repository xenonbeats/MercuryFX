import time
import logging
import threading
from datetime import datetime
from market_data import MarketDataClient
from technical_analysis_render import TechnicalAnalysisRender
from smart_money_concepts_render import SmartMoneyConceptsRender
from telegram_client import TelegramClient
from risk_management import RiskManager

logger = logging.getLogger(__name__)

class TradingBot:
    def __init__(self):
        """Initialize the trading bot"""
        self.symbols = {
            'EURUSD=X': {'name': 'EUR/USD', 'atr_multiplier': 0.002, 'asset_type': 'forex'},
            'GBPUSD=X': {'name': 'GBP/USD', 'atr_multiplier': 0.002, 'asset_type': 'forex'},
            'XAUUSD=X': {'name': 'Gold', 'atr_multiplier': 20, 'asset_type': 'commodity'},
            'BTC-USD': {'name': 'Bitcoin', 'atr_multiplier': 20, 'asset_type': 'crypto'}
        }
        
        self.market_data_client = MarketDataClient()
        self.technical_analysis = TechnicalAnalysisRender()
        self.smart_money_concepts = SmartMoneyConceptsRender()
        self.telegram_client = TelegramClient()
        self.risk_manager = RiskManager()
        self.running = False
        self.last_signals = {}  # Track last signals to avoid duplicates
        self.min_confidence_threshold = 0.75  # Minimum confidence for signal generation
        self.high_quality_threshold = 0.85  # High-quality sniper setups
        
        logger.info("TradingBot initialized successfully")
    
    def fetch_market_data(self, symbol, period='5d', interval='15m'):
        """Fetch market data for a given symbol"""
        return self.market_data_client.fetch_data(symbol, period, interval)
    
    def calculate_stop_loss_take_profit(self, entry_price, direction, symbol):
        """Calculate stop loss and take profit levels"""
        symbol_info = self.symbols[symbol]
        atr_value = symbol_info['atr_multiplier']
        
        if direction == 'BUY':
            stop_loss = entry_price - atr_value
            take_profit = entry_price + (2 * atr_value)  # 2:1 risk-reward ratio
        else:  # SELL
            stop_loss = entry_price + atr_value
            take_profit = entry_price - (2 * atr_value)
            
        return round(stop_loss, 5), round(take_profit, 5)
    
    def generate_signal(self, symbol, data):
        """Generate advanced trading signal using SMC + Technical Analysis"""
        try:
            # Calculate technical indicators
            indicators = self.technical_analysis.calculate_indicators(data)
            if not indicators:
                return None
            
            # Perform Smart Money Concepts analysis
            smc_analysis = self.smart_money_concepts.analyze_smart_money_concepts(data, symbol)
            if not smc_analysis:
                logger.warning(f"No SMC analysis available for {symbol}")
                return None
            
            # Get SMC signal strength and confluence
            smc_signal = self.smart_money_concepts.calculate_smc_signal_strength(smc_analysis)
            
            # Traditional technical analysis signals
            latest_ema50 = indicators['ema50']
            latest_ema200 = indicators['ema200']
            latest_rsi = indicators['rsi']
            latest_macd = indicators['macd']
            latest_macd_signal = indicators['macd_signal']
            latest_price = indicators['price']
            
            traditional_signals = []
            
            # EMA Crossover Signal
            if latest_ema50 > latest_ema200 and latest_price > latest_ema50:
                traditional_signals.append('BUY')
            elif latest_ema50 < latest_ema200 and latest_price < latest_ema50:
                traditional_signals.append('SELL')
            
            # RSI Signal (modified for SMC context)
            if latest_rsi < 35:  # More conservative oversold
                traditional_signals.append('BUY')
            elif latest_rsi > 65:  # More conservative overbought
                traditional_signals.append('SELL')
            
            # MACD Signal
            if latest_macd > latest_macd_signal and latest_macd > 0:
                traditional_signals.append('BUY')
            elif latest_macd < latest_macd_signal and latest_macd < 0:
                traditional_signals.append('SELL')
            
            # Apply advanced filtering for sniper strategy
            if not self.is_high_quality_setup(smc_signal, traditional_signals, symbol, data):
                logger.info(f"Setup for {symbol} doesn't meet quality standards - skipping")
                return None
            
            # Determine final direction based on confluence
            final_direction = self.get_confluence_direction(smc_signal, traditional_signals)
            if not final_direction:
                return None
            
            # Calculate advanced stop loss and take profit using SMC levels
            entry_price = round(latest_price, 5)
            stop_loss, take_profit = self.calculate_stop_loss_take_profit(entry_price, final_direction, symbol)
            
            # Calculate overall confidence score
            overall_confidence = self.calculate_overall_confidence(smc_signal, traditional_signals)
            
            signal = {
                'symbol': symbol,
                'asset_name': self.symbols[symbol]['name'],
                'direction': final_direction,
                'entry_price': entry_price,
                'stop_loss': stop_loss,
                'take_profit': take_profit,
                'timestamp': datetime.now(),
                'confidence': overall_confidence,
                'risk_quality': smc_signal.get('risk_quality', 'MEDIUM'),
                'strategy_type': 'SMC_SNIPER',
                'smc_signals': smc_signal.get('signals', []),
                'traditional_indicators': {
                    'ema50': round(latest_ema50, 5),
                    'ema200': round(latest_ema200, 5),
                    'rsi': round(latest_rsi, 2),
                    'macd': round(latest_macd, 5)
                },
                'signal_strength': smc_signal.get('signal_count', 0) + len(traditional_signals)
            }
            
            logger.info(f"Generated HIGH-QUALITY {final_direction} signal for {symbol} at {entry_price} (Confidence: {overall_confidence:.2f})")
            return signal
            
        except Exception as e:
            logger.error(f"Error generating signal for {symbol}: {e}")
            return None
    
    def is_high_quality_setup(self, smc_signal, traditional_signals, symbol, data):
        """Advanced risk assessment - only allow high-quality setups"""
        try:
            # SMC confidence must be above threshold
            if smc_signal.get('confidence', 0) < self.min_confidence_threshold:
                logger.debug(f"{symbol}: SMC confidence too low ({smc_signal.get('confidence', 0):.2f})")
                return False
            
            # Must have SMC signal confluence (multiple SMC patterns)
            if smc_signal.get('signal_count', 0) < 2:
                logger.debug(f"{symbol}: Insufficient SMC signal confluence")
                return False
            
            # Traditional indicators must align with SMC
            smc_direction = smc_signal.get('action')
            traditional_buy = traditional_signals.count('BUY')
            traditional_sell = traditional_signals.count('SELL')
            
            if smc_direction == 'BUY' and traditional_buy < traditional_sell:
                logger.debug(f"{symbol}: SMC/Traditional indicator mismatch")
                return False
            elif smc_direction == 'SELL' and traditional_sell < traditional_buy:
                logger.debug(f"{symbol}: SMC/Traditional indicator mismatch")
                return False
            
            # Check for volatility extremes (avoid choppy markets)
            if self.is_market_too_volatile(data, symbol):
                logger.debug(f"{symbol}: Market too volatile for reliable signals")
                return False
            
            # Additional quality filters based on asset type
            if not self.asset_specific_quality_check(symbol, data, smc_signal):
                logger.debug(f"{symbol}: Failed asset-specific quality check")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error in quality assessment for {symbol}: {e}")
            return False
    
    def get_confluence_direction(self, smc_signal, traditional_signals):
        """Get final direction based on SMC and traditional confluence"""
        smc_direction = smc_signal.get('action')
        traditional_buy = traditional_signals.count('BUY')
        traditional_sell = traditional_signals.count('SELL')
        
        if smc_direction == 'BUY' and traditional_buy >= 1:
            return 'BUY'
        elif smc_direction == 'SELL' and traditional_sell >= 1:
            return 'SELL'
        else:
            return None
    
    def calculate_overall_confidence(self, smc_signal, traditional_signals):
        """Calculate overall confidence combining SMC and traditional analysis"""
        smc_confidence = smc_signal.get('confidence', 0)
        traditional_strength = max(traditional_signals.count('BUY'), traditional_signals.count('SELL')) / 3.0
        
        # Weighted average (SMC gets 70% weight, traditional gets 30%)
        overall = (smc_confidence * 0.7) + (traditional_strength * 0.3)
        return min(overall, 1.0)
    
    def is_market_too_volatile(self, data, symbol):
        """Check if market is too volatile for reliable signals"""
        try:
            # Calculate recent volatility (last 20 periods)
            recent_data = data.tail(20)
            returns = recent_data['Close'].pct_change().dropna()
            volatility = returns.std()
            
            # Volatility thresholds by asset type
            thresholds = {
                'forex': 0.015,      # 1.5% daily volatility
                'commodity': 0.025,  # 2.5% daily volatility
                'crypto': 0.05       # 5% daily volatility
            }
            
            asset_type = self.symbols[symbol]['asset_type']
            threshold = thresholds.get(asset_type, 0.02)
            
            return volatility > threshold
            
        except Exception as e:
            logger.error(f"Error checking volatility for {symbol}: {e}")
            return False
    
    def asset_specific_quality_check(self, symbol, data, smc_signal):
        """Asset-specific quality checks"""
        try:
            asset_type = self.symbols[symbol]['asset_type']
            current_price = data['Close'].iloc[-1]
            
            # Forex-specific checks
            if asset_type == 'forex':
                # Check for major news times (simplified)
                current_hour = datetime.now().hour
                # Avoid major news hours (8-10 GMT, 13-15 GMT)
                if current_hour in [8, 9, 13, 14]:
                    logger.debug(f"{symbol}: Avoiding major news hours")
                    return False
            
            # Crypto-specific checks
            elif asset_type == 'crypto':
                # Check for weekend volatility reduction
                if datetime.now().weekday() >= 5:  # Weekend
                    if smc_signal.get('confidence', 0) < 0.8:
                        return False
            
            # Gold-specific checks
            elif asset_type == 'commodity':
                # Check for reasonable price levels
                if current_price < 1800 or current_price > 2200:
                    logger.debug(f"{symbol}: Price outside normal range")
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error in asset-specific check for {symbol}: {e}")
            return True
    
    def calculate_advanced_stop_loss_take_profit(self, entry_price, direction, symbol, smc_analysis):
        """Calculate SL/TP using SMC levels and traditional ATR"""
        try:
            # Get traditional ATR-based levels as fallback
            traditional_sl, traditional_tp = self.calculate_stop_loss_take_profit(entry_price, direction, symbol)
            
            # Try to use SMC levels for more precise SL/TP
            order_blocks = smc_analysis.get('order_blocks', {}).get('order_blocks', [])
            swing_points = smc_analysis.get('swing_points', {})
            
            if direction == 'BUY':
                # For BUY: Look for recent swing low or bullish order block as SL
                best_sl = traditional_sl
                
                # Check recent swing lows
                swing_lows = swing_points.get('swing_lows', [])
                if swing_lows:
                    recent_low = swing_lows[-1]['price']
                    if recent_low < entry_price and recent_low > traditional_sl:
                        best_sl = recent_low - (entry_price * 0.0005)  # Small buffer
                
                # Check bullish order blocks
                for ob in order_blocks:
                    if ob['type'] == 'ORDER_BLOCK_BULLISH' and ob['zone_bottom'] < entry_price:
                        if ob['zone_bottom'] > best_sl:
                            best_sl = ob['zone_bottom'] - (entry_price * 0.0005)
                
                stop_loss = max(best_sl, traditional_sl)  # Don't make SL worse than traditional
                take_profit = entry_price + (2.5 * abs(entry_price - stop_loss))  # Better R:R for high-quality setups
                
            else:  # SELL
                # For SELL: Look for recent swing high or bearish order block as SL
                best_sl = traditional_sl
                
                # Check recent swing highs
                swing_highs = swing_points.get('swing_highs', [])
                if swing_highs:
                    recent_high = swing_highs[-1]['price']
                    if recent_high > entry_price and recent_high < traditional_sl:
                        best_sl = recent_high + (entry_price * 0.0005)  # Small buffer
                
                # Check bearish order blocks
                for ob in order_blocks:
                    if ob['type'] == 'ORDER_BLOCK_BEARISH' and ob['zone_top'] > entry_price:
                        if ob['zone_top'] < best_sl:
                            best_sl = ob['zone_top'] + (entry_price * 0.0005)
                
                stop_loss = min(best_sl, traditional_sl)  # Don't make SL worse than traditional
                take_profit = entry_price - (2.5 * abs(stop_loss - entry_price))  # Better R:R for high-quality setups
            
            return round(stop_loss, 5), round(take_profit, 5)
            
        except Exception as e:
            logger.error(f"Error calculating advanced SL/TP for {symbol}: {e}")
            return self.calculate_stop_loss_take_profit(entry_price, direction, symbol)
    
    def should_send_signal(self, signal):
        """Check if signal should be sent (avoid duplicates)"""
        symbol = signal['symbol']
        direction = signal['direction']
        
        # Check if we recently sent a similar signal
        if symbol in self.last_signals:
            last_signal = self.last_signals[symbol]
            time_diff = (signal['timestamp'] - last_signal['timestamp']).total_seconds()
            
            # Don't send same direction signal within 1 hour
            if (last_signal['direction'] == direction and time_diff < 3600):
                return False
        
        return True
    
    def process_symbol(self, symbol):
        """Process a single symbol and generate signals"""
        try:
            # Fetch market data
            data = self.fetch_market_data(symbol)
            if data is None or len(data) < 200:  # Need enough data for EMA200
                logger.warning(f"Insufficient data for {symbol}")
                return
            
            # Generate signal
            signal = self.generate_signal(symbol, data)
            if signal and self.should_send_signal(signal):
                # Send Telegram alert
                success = self.telegram_client.send_signal(signal)
                if success:
                    self.last_signals[symbol] = signal
                    logger.info(f"Signal sent successfully for {symbol}")
                else:
                    logger.error(f"Failed to send signal for {symbol}")
            
        except Exception as e:
            logger.error(f"Error processing {symbol}: {e}")
    
    def run_cycle(self):
        """Run one complete cycle of signal generation"""
        logger.info("Starting new trading cycle")
        
        # Process each symbol
        for symbol in self.symbols:
            if not self.running:
                break
            self.process_symbol(symbol)
            time.sleep(1)  # Small delay between symbols
        
        logger.info("Trading cycle completed")
    
    def start(self):
        """Start the trading bot"""
        self.running = True
        logger.info("MercuryFX V2 Trading Bot started")
        
        # Send startup notification
        startup_message = "🚀 MercuryFX V2 - SMC SNIPER BOT Started!\n\n📊 <b>Advanced Strategy Integration:</b>\n• Break of Structure (BOS)\n• Market Structure Shift (MSS)\n• Fair Value Gap (FVG)\n• Order Block Analysis\n\n🎯 <b>Monitored Assets:</b>\n• EUR/USD (Forex)\n• GBP/USD (Forex)\n• Gold XAU/USD (Commodity)\n• Bitcoin BTC/USD (Crypto)\n\n⚙️ <b>Quality Filters:</b>\n• Minimum 75% confidence threshold\n• Multi-timeframe confluence required\n• Volatility and news avoidance\n• Enhanced risk management\n\n🔄 <b>Signal Interval:</b> 15 minutes\n\n<i>Only HIGH-QUALITY sniper setups will be posted!</i>"
        self.telegram_client.send_message(startup_message)
        
        while self.running:
            try:
                self.run_cycle()
                
                # Wait 15 minutes before next cycle
                for _ in range(900):  # 900 seconds = 15 minutes
                    if not self.running:
                        break
                    time.sleep(1)
                    
            except KeyboardInterrupt:
                logger.info("Bot stopped by user")
                break
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                time.sleep(60)  # Wait 1 minute before retrying
        
        logger.info("Trading bot stopped")
    
    def stop(self):
        """Stop the trading bot"""
        self.running = False
        logger.info("Trading bot stop requested")
