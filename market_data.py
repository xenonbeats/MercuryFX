import requests
import json
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class MarketDataClient:
    def __init__(self):
        """Initialize market data client using direct API calls"""
        self.base_url = "https://query1.finance.yahoo.com/v8/finance/chart"
        
    def fetch_data(self, symbol, period='5d', interval='15m'):
        """Fetch market data directly from Yahoo Finance API"""
        try:
            url = f"{self.base_url}/{symbol}"
            params = {
                'period1': self._get_timestamp_days_ago(5),
                'period2': self._get_current_timestamp(),
                'interval': interval,
                'includePrePost': 'true',
                'events': 'div%2Csplit'
            }
            
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            if 'chart' not in data or 'result' not in data['chart']:
                logger.error(f"Invalid response format for {symbol}")
                return None
                
            result = data['chart']['result'][0]
            
            if 'timestamp' not in result or not result['indicators']['quote']:
                logger.error(f"No data available for {symbol}")
                return None
                
            timestamps = result['timestamp']
            quotes = result['indicators']['quote'][0]
            
            # Convert to simple dict format
            market_data = {
                'timestamps': timestamps,
                'open': quotes['open'],
                'high': quotes['high'],
                'low': quotes['low'],
                'close': quotes['close'],
                'volume': quotes['volume']
            }
            
            # Filter out None values
            valid_data = self._clean_data(market_data)
            
            if len(valid_data['close']) < 50:
                logger.warning(f"Insufficient data points for {symbol}: {len(valid_data['close'])}")
                return None
                
            logger.info(f"Successfully fetched {len(valid_data['close'])} data points for {symbol}")
            return valid_data
            
        except Exception as e:
            logger.error(f"Error fetching data for {symbol}: {e}")
            return None
    
    def _get_current_timestamp(self):
        """Get current timestamp"""
        return int(datetime.now().timestamp())
    
    def _get_timestamp_days_ago(self, days):
        """Get timestamp for days ago"""
        return int((datetime.now() - timedelta(days=days)).timestamp())
    
    def _clean_data(self, data):
        """Remove None values from data"""
        cleaned = {
            'timestamps': [],
            'open': [],
            'high': [],
            'low': [],
            'close': [],
            'volume': []
        }
        
        for i in range(len(data['timestamps'])):
            if (data['close'][i] is not None and 
                data['open'][i] is not None and 
                data['high'][i] is not None and 
                data['low'][i] is not None):
                
                cleaned['timestamps'].append(data['timestamps'][i])
                cleaned['open'].append(data['open'][i])
                cleaned['high'].append(data['high'][i])
                cleaned['low'].append(data['low'][i])
                cleaned['close'].append(data['close'][i])
                cleaned['volume'].append(data['volume'][i] or 0)
        
        return cleaned