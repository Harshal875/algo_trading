"""
Trading Strategy - RSI + Moving Average Strategy
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'data'))

from data_fetcher import DataFetcher
from indicators import TechnicalIndicators

class TradingStrategy:
    def __init__(self):
        print("Trading Strategy initialized!")
        self.data_fetcher = DataFetcher()
        self.indicators = TechnicalIndicators()
    
    def analyze_stock(self, symbol):
        """Analyze one stock and return buy/sell/hold signal"""
        print(f"Analyzing {symbol}...")
        
        # Get 6 months of data
        data = self.data_fetcher.fetch_one_stock(symbol)
        
        # Calculate indicators
        rsi = self.indicators.calculate_rsi(data['Close'])
        ma20, ma50 = self.indicators.calculate_moving_averages(data['Close'])
        
        # Get latest values
        latest_rsi = float(rsi.iloc[-1])
        latest_ma20 = float(ma20.iloc[-1])
        latest_ma50 = float(ma50.iloc[-1])
        latest_price = float(data['Close'].iloc[-1])
        
        # Apply strategy: RSI < 30 AND MA20 > MA50
        signal = "BUY" if (latest_rsi < 30 and latest_ma20 > latest_ma50) else "HOLD"
        
        return {
            'symbol': symbol,
            'price': latest_price,
            'rsi': latest_rsi,
            'ma20': latest_ma20,
            'ma50': latest_ma50,
            'signal': signal
        }

# Test it
if __name__ == "__main__":
    strategy = TradingStrategy()
    
    # Test on our 3 stocks
    stocks = ["RELIANCE.NS", "TCS.NS", "INFY.NS"]
    
    print("\n" + "="*60)
    print("TRADING SIGNALS")
    print("="*60)
    
    for stock in stocks:
        result = strategy.analyze_stock(stock)
        print(f"{result['symbol']}: {result['signal']} at ₹{result['price']:.0f} (RSI: {result['rsi']:.1f})")