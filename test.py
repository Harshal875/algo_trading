# Create a simple test file: test_performance.py
from src.automation.sheets_manager import SheetsManager

# Test just the performance metrics
sheets = SheetsManager()

# Replace with your actual sheet URL
SHEET_URL = "https://docs.google.com/spreadsheets/d/1-4y8RLos22VonrtcEMpZK6-rM6pFgTt3NmFYFKQkb7A/edit?gid=1432976107#gid=1432976107"

if not sheets.mock_mode:
    sheets.connect_to_sheet(SHEET_URL)
    
    # Test performance update with simpler data
    performance_data = [
        {'stock': 'RELIANCE.NS', 'return': -0.8, 'trades': 2, 'win_rate': 0},
        {'stock': 'TCS.NS', 'return': 0.7, 'trades': 2, 'win_rate': 50}
    ]
    
    print("Testing Performance Metrics update...")
    sheets.update_performance(performance_data)
    print("Done!")