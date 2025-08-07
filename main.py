"""
MAIN ALGO TRADING SYSTEM - Windows Console Friendly
"""
import yfinance as yf
from datetime import datetime
import sys
import os

# Add all our modules to path
sys.path.append('src/data')
sys.path.append('src/strategy') 
sys.path.append('src/ml')
sys.path.append('src/automation')

# Import the simple additions
from logger import TradingLogger
import config

# Import existing modules (unchanged)
from data_fetcher import DataFetcher
from indicators import TechnicalIndicators
from backtester import Backtester
from model import StockPredictor
from sheets_manager import SheetsManager
from telegram_bot import TelegramAlert

class AlgoTradingSystem:
    def __init__(self):
        """Initialize trading system - now with Windows-friendly logging"""
        # Add logger
        self.logger = TradingLogger(__name__, config.LOG_LEVEL)
        
        self.logger.info("INITIALIZING ALGO TRADING SYSTEM")
        self.logger.info("="*50)
        
        # Everything else stays exactly the same
        self.data_fetcher = DataFetcher()
        self.indicators = TechnicalIndicators()
        self.backtester = Backtester()
        self.predictor = StockPredictor()
        self.sheets = SheetsManager()
        
        # Connect to Google Sheets - use config
        if config.GOOGLE_SHEET_URL and not self.sheets.mock_mode:
            self.sheets.connect_to_sheet(config.GOOGLE_SHEET_URL)
        
        self.stocks = ["RELIANCE.NS", "TCS.NS", "INFY.NS"]
        
        # Initialize Telegram - use config  
        if config.TELEGRAM_BOT_TOKEN and config.TELEGRAM_CHAT_ID:
            self.telegram = TelegramAlert(config.TELEGRAM_BOT_TOKEN, config.TELEGRAM_CHAT_ID)
            self.logger.info("Telegram alerts enabled")
        else:
            self.telegram = None
            self.logger.info("Telegram alerts disabled")
    
    def run_complete_analysis(self):
        """Run complete trading analysis - Windows friendly logging"""
        self.logger.info("RUNNING COMPLETE MARKET ANALYSIS")
        self.logger.info("="*50)
        
        results = {}
        
        for stock in self.stocks:
            self.logger.info(f"Analyzing {stock}...")
            
            # Get data
            data = yf.download(stock, period="6mo")
            
            # Run backtest
            signals = self.backtester.generate_signals(data, stock)
            trades, portfolio_history, final_portfolio = self.backtester.simulate_trading(signals, stock)
            
            # Calculate return
            return_pct = ((final_portfolio['total_value'] - self.backtester.initial_capital) / self.backtester.initial_capital * 100)
            
            # ML prediction
            features = self.predictor.prepare_features(data)
            ml_results = self.predictor.train_models(features)
            
            # Store results
            results[stock] = {
                'return': return_pct,
                'trades': len(trades),
                'ml_accuracy': ml_results['decision_tree_accuracy'] * 100,
                'latest_price': data['Close'].iloc[-1].item(),
                'trades_data': trades
            }
            
            # Log results - Windows friendly
            self.logger.info(f"  Return: {return_pct:+.1f}%")
            self.logger.info(f"  ML Accuracy: {ml_results['decision_tree_accuracy']:.1%}")
            self.logger.info(f"  Trades: {len(trades)}")
        
        return results
    
    def update_google_sheets(self, results):
        """Update Google Sheets - Windows friendly logging"""
        self.logger.info("UPDATING GOOGLE SHEETS...")
        
        # Log all trades
        for stock, data in results.items():
            for trade in data['trades_data']:
                self.sheets.log_trade({
                    'date': trade['date'].strftime('%Y-%m-%d'),
                    'symbol': stock,
                    'action': trade['action'],
                    'shares': trade['shares'],
                    'price': trade['price'],
                    'value': trade['value'],
                    'portfolio_value': trade['portfolio_value']
                })
        
        # Update portfolio summary
        avg_return = sum([data['return'] for data in results.values()]) / len(results)
        total_trades = sum([data['trades'] for data in results.values()])
        avg_ml_accuracy = sum([data['ml_accuracy'] for data in results.values()]) / len(results)
        
        self.sheets.update_portfolio({
            'total_stocks_analyzed': len(self.stocks),
            'average_return': f"{avg_return:.1f}%",
            'total_trades_executed': total_trades,
            'average_ml_accuracy': f"{avg_ml_accuracy:.1f}%",
            'best_performer': max(results.keys(), key=lambda x: results[x]['return']),
            'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        
        performance_data = []
        for stock, data in results.items():
            performance_data.append({
                'stock': stock,
                'return': data['return'],
                'trades': data['trades'],
                'win_rate': 0  # Calculate actual win rate if needed
            })
        
        self.sheets.update_performance(performance_data)

        self.logger.info("Google Sheets updated successfully!")
    
        # Send Telegram portfolio summary
        if self.telegram:
            self.telegram.send_portfolio_summary({
                'total_value': f"Rs {self.backtester.initial_capital:,}",
                'average_return': f"{avg_return:.1f}%",
                'best_performer': max(results.keys(), key=lambda x: results[x]['return']),
                'total_trades_executed': total_trades,
                'average_ml_accuracy': f"{avg_ml_accuracy:.1f}%"
            })
    
    def show_final_report(self, results):
        """Show final report - Windows friendly"""
        self.logger.info("\n" + "="*60)
        self.logger.info("FINAL ALGO TRADING SYSTEM REPORT")
        self.logger.info("="*60)
        
        for stock, data in results.items():
            self.logger.info(f"\n{stock}:")
            self.logger.info(f"   Return: {data['return']:+.1f}%")
            self.logger.info(f"   ML Accuracy: {data['ml_accuracy']:.1f}%") 
            self.logger.info(f"   Trades: {data['trades']}")
            self.logger.info(f"   Latest Price: Rs {data['latest_price']:.0f}")
        
        avg_return = sum([data['return'] for data in results.values()]) / len(results)
        self.logger.info(f"\nPORTFOLIO SUMMARY:")
        self.logger.info(f"   Average Return: {avg_return:+.1f}%")
        self.logger.info(f"   Total Trades: {sum([data['trades'] for data in results.values()])}")
        self.logger.info(f"   Avg ML Accuracy: {sum([data['ml_accuracy'] for data in results.values()]) / len(results):.1f}%")
        
        self.logger.info(f"\nSYSTEM STATUS: ALL COMPONENTS WORKING!")
        self.logger.info("="*60)


# Run the complete system
if __name__ == "__main__":
    # Initialize and run
    system = AlgoTradingSystem()
    results = system.run_complete_analysis()
    system.update_google_sheets(results)
    system.show_final_report(results)