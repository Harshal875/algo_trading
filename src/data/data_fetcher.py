"""
Simple Data Fetcher - Step by step build
"""
import yfinance as yf
import pandas as pd

class DataFetcher:
    def __init__(self):
        print("DataFetcher initialized!")
        # Our 3 NIFTY stocks for the project
        self.stocks = ["RELIANCE.NS", "TCS.NS", "INFY.NS"]
    
    def fetch_one_stock(self, symbol):
        """Fetch data for one stock"""
        print(f"Fetching data for {symbol}...")
        data = yf.download(symbol, period="1mo")
        print(f"Got {len(data)} days of data")
        return data
    
    def fetch_three_stocks(self):
        """Fetch data for our 3 main stocks"""
        all_data = {}
        for stock in self.stocks:
            print(f"\nFetching {stock}...")
            data = yf.download(stock, period="6mo")  # 6 months for backtesting
            all_data[stock] = data
            print(f"✓ {stock}: {len(data)} days")
        return all_data


# Test it
# Test it
if __name__ == "__main__":
    fetcher = DataFetcher()
    
    print("\n" + "="*50)
    print("Testing 3 stocks fetch...")
    
    data = fetcher.fetch_three_stocks()
    
    print("\n" + "="*50)
    print("Summary:")
    for stock, df in data.items():
        # Fix: Convert to float
        latest_price = float(df['Close'].iloc[-1])
        print(f"{stock}: ₹{latest_price:.2f} ({len(df)} days)")