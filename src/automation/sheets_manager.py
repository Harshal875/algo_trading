"""
Google Sheets Manager - REAL Google Sheets Integration
"""
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from datetime import datetime
import os

class SheetsManager:
    def __init__(self, credentials_file='credentials.json', sheet_url=None):
        """Initialize Google Sheets connection"""
        print("Initializing Google Sheets Manager...")
        
        # Check if credentials file exists
        if os.path.exists(credentials_file):
            try:
                # Set up credentials
                scope = ['https://spreadsheets.google.com/feeds',
                        'https://www.googleapis.com/auth/drive']
                
                credentials = ServiceAccountCredentials.from_json_keyfile_name(
                    credentials_file, scope)
                
                # Connect to Google Sheets
                self.gc = gspread.authorize(credentials)
                self.mock_mode = False
                print("✅ Connected to Google Sheets!")
                
                # If sheet URL provided, connect to it
                if sheet_url:
                    self.sheet = self.gc.open_by_url(sheet_url)
                    print(f"✅ Connected to sheet: {self.sheet.title}")
                else:
                    self.sheet = None
                    
            except Exception as e:
                print(f"❌ Error connecting to Google Sheets: {e}")
                print("Running in MOCK mode")
                self.mock_mode = True
        else:
            print("❌ credentials.json not found - Running in MOCK mode")
            self.mock_mode = True
        
        # Mock data storage
        self.trade_log = []
        self.portfolio_summary = {}
    
    def connect_to_sheet(self, sheet_url):
        """Connect to a specific Google Sheet"""
        if self.mock_mode:
            print(f"MOCK: Would connect to {sheet_url}")
            return True
            
        try:
            self.sheet = self.gc.open_by_url(sheet_url)
            print(f"✅ Connected to sheet: {self.sheet.title}")
            
            # Initialize sheet headers
            self.setup_sheet_headers()
            return True
            
        except Exception as e:
            print(f"❌ Error connecting to sheet: {e}")
            return False
    
    def setup_sheet_headers(self):
        """Set up headers for all tabs"""
        if self.mock_mode:
            print("MOCK: Setting up headers")
            return
            
        try:
            # Trade Log headers
            trade_sheet = self.sheet.worksheet("Trade Log")
            trade_headers = ["Date", "Symbol", "Action", "Shares", "Price", "Value", "Portfolio_Value"]
            trade_sheet.insert_row(trade_headers, 1)
            
            # Portfolio Summary headers
            portfolio_sheet = self.sheet.worksheet("Portfolio Summary")
            portfolio_headers = ["Metric", "Value", "Last_Updated"]
            portfolio_sheet.insert_row(portfolio_headers, 1)
            
            # Performance Metrics headers
            performance_sheet = self.sheet.worksheet("Performance Metrics")
            performance_headers = ["Stock", "Total_Return", "Trades", "Win_Rate", "Last_Updated"]
            performance_sheet.insert_row(performance_headers, 1)
            
            print("✅ Sheet headers initialized")
            
        except Exception as e:
            print(f"⚠️ Headers may already exist: {e}")
    
    def log_trade(self, trade_data):
        """Log a trade to Google Sheets"""
        if self.mock_mode:
            print(f"📊 MOCK TRADE: {trade_data}")
            self.trade_log.append(trade_data)
            return
        
        try:
            trade_sheet = self.sheet.worksheet("Trade Log")
            
            # Prepare row data
            row = [
                trade_data.get('date', ''),
                trade_data.get('symbol', ''),
                trade_data.get('action', ''),
                trade_data.get('shares', 0),
                trade_data.get('price', 0),
                trade_data.get('value', 0),
                trade_data.get('portfolio_value', 0)
            ]
            
            trade_sheet.append_row(row)
            print(f"✅ Trade logged to Google Sheets")
            
        except Exception as e:
            print(f"❌ Error logging trade: {e}")
    
    def update_portfolio(self, portfolio_data):
        """Update portfolio summary in Google Sheets"""
        if self.mock_mode:
            print(f"💼 MOCK PORTFOLIO: {portfolio_data}")
            self.portfolio_summary = portfolio_data
            return
        
        try:
            portfolio_sheet = self.sheet.worksheet("Portfolio Summary")
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Clear existing data (except headers)
            portfolio_sheet.clear()
            headers = ["Metric", "Value", "Last_Updated"]
            portfolio_sheet.insert_row(headers, 1)
            
            # Add portfolio data
            for key, value in portfolio_data.items():
                row = [key.replace('_', ' ').title(), str(value), timestamp]
                portfolio_sheet.append_row(row)
            
            print(f"✅ Portfolio updated in Google Sheets")
            
        except Exception as e:
            print(f"❌ Error updating portfolio: {e}")
    
    def update_performance(self, performance_data):
        """Update performance metrics"""
        if self.mock_mode:
            print(f"📈 MOCK PERFORMANCE: {performance_data}")
            return
        
        try:
            performance_sheet = self.sheet.worksheet("Performance Metrics")
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Clear existing data (except headers)
            performance_sheet.clear()
            headers = ["Stock", "Total_Return", "Trades", "Win_Rate", "Last_Updated"]
            performance_sheet.insert_row(headers, 1)
            
            # Add performance data
            for stock_data in performance_data:
                row = [
                    stock_data.get('stock', ''),
                    f"{stock_data.get('return', 0):.1f}%",
                    stock_data.get('trades', 0),
                    f"{stock_data.get('win_rate', 0):.1f}%",
                    timestamp
                ]
                performance_sheet.append_row(row)
            
            print(f"✅ Performance metrics updated")
            
        except Exception as e:
            print(f"❌ Error updating performance: {e}")
    
    def show_summary(self):
        """Show current summary"""
        print(f"\n📈 SUMMARY:")
        if self.mock_mode:
            print(f"Trade Log: {len(self.trade_log)} trades")
            print(f"Portfolio: {self.portfolio_summary}")
        else:
            print(f"Google Sheets: {self.sheet.title if self.sheet else 'Not connected'}")

# Test it
if __name__ == "__main__":
    # PASTE YOUR GOOGLE SHEET URL HERE
    SHEET_URL = "https://docs.google.com/spreadsheets/d/1-4y8RLos22VonrtcEMpZK6-rM6pFgTt3NmFYFKQkb7A/edit?gid=1157482854#gid=1157482854"
    
    sheets = SheetsManager()
    
    # Connect to your sheet
    if not sheets.mock_mode:
        sheets.connect_to_sheet(SHEET_URL)
    
    # Test logging trades
    sheets.log_trade({
        'date': '2025-08-07',
        'symbol': 'RELIANCE.NS',
        'action': 'BUY',
        'shares': 20,
        'price': 1429,
        'value': 28580,
        'portfolio_value': 100000
    })
    
    # Test portfolio update
    sheets.update_portfolio({
        'total_value': 99246,
        'cash': 99246,
        'total_return': -0.8,
        'best_stock': 'TCS.NS (+0.7%)',
        'worst_stock': 'RELIANCE.NS (-0.8%)'
    })
    
    # Test performance update
    sheets.update_performance([
        {'stock': 'RELIANCE.NS', 'return': -0.8, 'trades': 2, 'win_rate': 0},
        {'stock': 'TCS.NS', 'return': 0.7, 'trades': 2, 'win_rate': 50},
        {'stock': 'INFY.NS', 'return': -0.7, 'trades': 2, 'win_rate': 0}
    ])
    
    sheets.show_summary()