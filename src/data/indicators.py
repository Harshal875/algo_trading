"""
Technical Indicators - Step by step build
"""
import pandas as pd
import numpy as np

class TechnicalIndicators:
    def __init__(self):
        print("TechnicalIndicators initialized!")
    
    def calculate_rsi(self, prices, period=14):
        """
        Calculate RSI (Relative Strength Index)
        RSI < 30 = Oversold (BUY signal)
        RSI > 70 = Overbought (SELL signal)
        """
        print(f"Calculating RSI with {period} days period...")
        
        # Calculate price changes
        delta = prices.diff()
        
        # Separate gains and losses
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        
        # Calculate RSI
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    
    def calculate_moving_averages(self, prices, short_window=20, long_window=50):
        """
        Calculate moving averages
        Our strategy: 20-DMA crossing above 50-DMA = Bullish signal
        """
        print(f"Calculating {short_window}-day and {long_window}-day moving averages...")
        
        ma_short = prices.rolling(window=short_window).mean()
        ma_long = prices.rolling(window=long_window).mean()
        
        return ma_short, ma_long


# Test it
if __name__ == "__main__":
    import yfinance as yf  # Direct import for testing
    
    # Get 6 months data (need this for 50-day MA)
    print("Fetching 6 months data for moving averages...")
    data = yf.download("RELIANCE.NS", period="6mo")
    print(f"Got {len(data)} days of data")
    
    # Test indicators
    indicators = TechnicalIndicators()
    rsi = indicators.calculate_rsi(data['Close'])
    ma20, ma50 = indicators.calculate_moving_averages(data['Close'])
    
    print(f"\nLast 5 days analysis for RELIANCE:")
    print("Date\t\tPrice\tRSI\tMA20\tMA50\tSignal")
    print("-" * 70)
    
    for i in range(-5, 0):
        date = rsi.index[i].strftime('%Y-%m-%d')
        price = float(data['Close'].iloc[i])
        rsi_val = float(rsi.iloc[i])
        ma20_val = float(ma20.iloc[i])
        ma50_val = float(ma50.iloc[i])
        
        # Our strategy: RSI < 30 AND MA20 > MA50
        rsi_signal = rsi_val < 30
        ma_signal = ma20_val > ma50_val
        final_signal = "BUY" if (rsi_signal and ma_signal) else "HOLD"
        
        print(f"{date}\t₹{price:.0f}\t{rsi_val:.1f}\t₹{ma20_val:.0f}\t₹{ma50_val:.0f}\t{final_signal}")