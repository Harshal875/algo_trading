"""
Backtesting Engine - Realistic P&L Simulation
"""
import pandas as pd
import numpy as np
from datetime import datetime
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'data'))

from data_fetcher import DataFetcher
from indicators import TechnicalIndicators

class Backtester:
    def __init__(self, initial_capital=100000):
        """
        Initialize backtester with starting money
        """
        print(f"Backtester initialized with ₹{initial_capital:,}")
        self.initial_capital = initial_capital
        self.data_fetcher = DataFetcher()
        self.indicators = TechnicalIndicators()
        
        # Trading parameters
        self.transaction_cost = 0.001  # 0.1% per trade (realistic)
        self.max_position_size = 0.3   # Max 30% of capital per stock
    
    def generate_signals(self, data, symbol):
        """
        Generate buy/sell signals with REALISTIC exit conditions
        """
        print(f"Generating signals for {symbol}...")
        
        # Calculate indicators
        rsi = self.indicators.calculate_rsi(data['Close'])
        ma20, ma50 = self.indicators.calculate_moving_averages(data['Close'])
        
        # Create signals DataFrame
        signals = pd.DataFrame(index=data.index)
        signals['Price'] = data['Close']
        signals['RSI'] = rsi
        signals['MA20'] = ma20
        signals['MA50'] = ma50
        signals['Signal'] = 0  # 0=Hold, 1=Buy, -1=Sell
        
        # Apply our strategy: RSI < 30 AND MA20 > MA50
        buy_condition = (signals['RSI'] < 30) & (signals['MA20'] > signals['MA50'])
        signals.loc[buy_condition, 'Signal'] = 1
        
        # REALISTIC sell conditions (multiple options):
        sell_condition = (
            (signals['RSI'] > 50) |  # Less strict than 70
            (signals['MA20'] < signals['MA50'])  # Trend reversal
        )
        signals.loc[sell_condition, 'Signal'] = -1
        
        # IMPORTANT: Add time-based exit (realistic for mini project)
        # After buy signal, force sell after 30 days if no other exit
        in_position = False
        buy_date = None
        
        for i, (date, row) in enumerate(signals.iterrows()):
            if row['Signal'] == 1 and not in_position:
                in_position = True
                buy_date = date
            elif row['Signal'] == -1 and in_position:
                in_position = False
                buy_date = None
            elif in_position and buy_date:
                # Check if 30 days passed since buy
                days_held = (date - buy_date).days
                if days_held >= 30:
                    signals.loc[date, 'Signal'] = -1  # Force sell
                    in_position = False
                    buy_date = None
        
        return signals
    
    def simulate_trading(self, signals, symbol):
        """
        Simulate actual trading with realistic P&L calculation
        """
        print(f"Simulating trading for {symbol}...")
        
        portfolio = {
            'cash': self.initial_capital,
            'shares': 0,
            'total_value': self.initial_capital
        }
        
        trades = []
        portfolio_history = []
        
        for date, row in signals.iterrows():
            signal = row['Signal']
            price = row['Price']
            
            # Calculate current portfolio value
            current_value = portfolio['cash'] + (portfolio['shares'] * price)
            portfolio['total_value'] = current_value
            
            # Record daily portfolio value
            portfolio_history.append({
                'date': date,
                'portfolio_value': current_value,
                'price': price,
                'cash': portfolio['cash'],
                'shares': portfolio['shares']
            })
            
            # Execute trades
            if signal == 1 and portfolio['shares'] == 0:  # BUY (only if not holding)
                # Calculate how many shares to buy (30% of portfolio)
                investment_amount = current_value * self.max_position_size
                shares_to_buy = int(investment_amount / price)
                
                if shares_to_buy > 0:
                    # Apply transaction cost
                    total_cost = shares_to_buy * price * (1 + self.transaction_cost)
                    
                    if total_cost <= portfolio['cash']:
                        portfolio['cash'] -= total_cost
                        portfolio['shares'] += shares_to_buy
                        
                        trades.append({
                            'date': date,
                            'action': 'BUY',
                            'shares': shares_to_buy,
                            'price': price,
                            'value': total_cost,
                            'portfolio_value': current_value
                        })
            
            elif signal == -1 and portfolio['shares'] > 0:  # SELL (only if holding)
                # Sell all shares
                total_sale = portfolio['shares'] * price * (1 - self.transaction_cost)
                portfolio['cash'] += total_sale
                
                trades.append({
                    'date': date,
                    'action': 'SELL',
                    'shares': portfolio['shares'],
                    'price': price,
                    'value': total_sale,
                    'portfolio_value': current_value
                })
                
                portfolio['shares'] = 0
        
        return trades, portfolio_history, portfolio

# Test the signal generation first
if __name__ == "__main__":
    import yfinance as yf
    
    backtester = Backtester()
    
    # Test with RELIANCE data - 6 months for proper backtesting
    print("Fetching 6 months of RELIANCE data...")
    data = yf.download("RELIANCE.NS", period="6mo")
    print(f"Got {len(data)} days of data")
    
    signals = backtester.generate_signals(data, "RELIANCE.NS")
    
    # Show signal summary
    buy_signals = signals[signals['Signal'] == 1]
    sell_signals = signals[signals['Signal'] == -1]
    
    print(f"\n📊 SIGNAL ANALYSIS for RELIANCE:")
    print(f"Total Buy Signals: {len(buy_signals)}")
    print(f"Total Sell Signals: {len(sell_signals)}")
    
    # RUN THE ACTUAL SIMULATION
    trades, portfolio_history, final_portfolio = backtester.simulate_trading(signals, "RELIANCE.NS")
    
    print(f"\n💰 TRADING RESULTS:")
    print(f"Initial Capital: ₹{backtester.initial_capital:,}")
    print(f"Final Portfolio Value: ₹{final_portfolio['total_value']:,.0f}")
    print(f"Total Return: {((final_portfolio['total_value'] - backtester.initial_capital) / backtester.initial_capital * 100):+.1f}%")
    print(f"Total Trades Executed: {len(trades)}")
    
    if len(trades) > 0:
        print(f"\n📈 TRADE HISTORY:")
        for trade in trades[:5]:  # Show first 5 trades
            print(f"  {trade['date'].strftime('%Y-%m-%d')}: {trade['action']} {trade['shares']} shares at ₹{trade['price']:.0f}")



    # TEST ALL 3 STOCKS (add this after the existing test)
    print("\n" + "="*70)
    print("PORTFOLIO PERFORMANCE - ALL 3 STOCKS")
    print("="*70)
    
    stocks = ["RELIANCE.NS", "TCS.NS", "INFY.NS"]
    total_returns = []
    
    for stock in stocks:
        print(f"\nTesting {stock}...")
        data = yf.download(stock, period="6mo")
        signals = backtester.generate_signals(data, stock)
        trades, portfolio_history, final_portfolio = backtester.simulate_trading(signals, stock)
        
        return_pct = ((final_portfolio['total_value'] - backtester.initial_capital) / backtester.initial_capital * 100)
        total_returns.append(return_pct)
        
        print(f"  {stock}: {return_pct:+.1f}% ({len(trades)} trades)")
    
    avg_return = sum(total_returns) / len(total_returns)
    print(f"\n🏆 PORTFOLIO SUMMARY:")
    print(f"Average Return Across 3 Stocks: {avg_return:+.1f}%")
    print(f"Best Performer: {max(total_returns):+.1f}%")
    print(f"Worst Performer: {min(total_returns):+.1f}%")