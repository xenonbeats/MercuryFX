# Render.com Package Error Fixes for MercuryFX V2

## 🚨 Common Package Issues & Solutions

### Issue 1: TA-Lib Installation Failure
**Error:** `ERROR: Failed building wheel for TA-Lib`
**Solution:** Use pre-compiled version or remove TA-Lib dependency

#### Option A: Remove TA-Lib (Recommended)
Update your `requirements.txt` to:
```txt
flask==3.0.3
gunicorn==23.0.0
numpy==1.26.4
pandas==2.2.2
python-dotenv==1.0.1
python-telegram-bot==21.4
requests==2.32.3
yfinance==0.2.28
ta==0.11.0
```

Then update `technical_analysis.py` to use `ta` library instead of `talib`:
```python
import ta
# Replace talib.EMA with ta.trend.ema_indicator
# Replace talib.RSI with ta.momentum.rsi
# Replace talib.MACD with ta.trend.macd
```

#### Option B: Alternative Requirements (if Option A fails)
```txt
flask==3.0.3
gunicorn==23.0.0
numpy==1.24.3
pandas==2.0.3
python-dotenv==1.0.0
python-telegram-bot==20.7
requests==2.31.0
yfinance==0.2.18
ta==0.10.2
```

### Issue 2: Build Timeout
**Error:** Build takes too long and times out
**Solution:** Simplify dependencies

Minimal requirements.txt:
```txt
flask==3.0.3
gunicorn==23.0.0
pandas==2.2.2
python-dotenv==1.0.1
python-telegram-bot==21.4
requests==2.32.3
yfinance==0.2.28
```

### Issue 3: Memory Issues During Build
**Error:** `Killed` or memory-related errors
**Solution:** Add these build optimizations

Create `.buildpacks` file:
```
https://github.com/heroku/heroku-buildpack-python.git
```

### Issue 4: Import Errors
**Error:** `ModuleNotFoundError` after successful build
**Solution:** Check your import statements

Update imports in `technical_analysis.py`:
```python
# Instead of: import talib
# Use: import ta

# Replace:
# df['ema50'] = talib.EMA(df['Close'], timeperiod=50)
# With:
df['ema50'] = ta.trend.ema_indicator(df['Close'], window=50)

# Replace:
# df['rsi'] = talib.RSI(df['Close'], timeperiod=14)
# With:
df['rsi'] = ta.momentum.rsi(df['Close'], window=14)

# Replace:
# macd, macd_signal, macd_histogram = talib.MACD(df['Close'])
# With:
df['macd'] = ta.trend.macd_diff(df['Close'])
df['macd_signal'] = ta.trend.macd_signal(df['Close'])
```

## 🛠️ Updated Code for Render Compatibility

### Modified technical_analysis.py (TA-Lib free):
```python
import logging
import pandas as pd
import ta

logger = logging.getLogger(__name__)

class TechnicalAnalysis:
    def __init__(self):
        logger.info("TechnicalAnalysis module initialized")
    
    def calculate_indicators(self, data):
        try:
            if len(data) < 200:
                logger.warning("Insufficient data for technical analysis")
                return None
            
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
            
            return indicators
            
        except Exception as e:
            logger.error(f"Error calculating indicators: {e}")
            return None
```

## 🔧 Step-by-Step Fix Process

1. **Update requirements.txt** - Use the minimal version above
2. **Update technical_analysis.py** - Replace talib with ta library
3. **Redeploy on Render** - Push changes to GitHub
4. **Monitor build logs** - Check for specific error messages
5. **Test functionality** - Verify indicators still work

## 📝 Debug Commands for Render Logs

Add these to your main.py for debugging:
```python
import sys
print(f"Python version: {sys.version}")
print("Installed packages:")
import subprocess
result = subprocess.run([sys.executable, "-m", "pip", "list"], capture_output=True, text=True)
print(result.stdout)
```

## 🚀 Quick Fix Summary

1. Replace your `requirements.txt` with the minimal version
2. Update `technical_analysis.py` to use `ta` instead of `talib`
3. Redeploy on Render
4. Check build logs for success

This should resolve the package installation issues on Render.com!