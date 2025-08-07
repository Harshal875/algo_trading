"""
Telegram Bot Integration for Trading Alerts
"""
import telegram
from telegram import Bot
import asyncio

class TelegramAlert:
    def __init__(self, bot_token, chat_id=None):
        """Initialize Telegram bot"""
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.bot = Bot(token=bot_token)
        print("📱 Telegram bot initialized!")
    
    def send_message(self, message):
        """Send message to Telegram"""
        try:
            if self.chat_id:
                asyncio.run(self.bot.send_message(chat_id=self.chat_id, text=message))
                print(f"✅ Telegram message sent!")
            else:
                print(f"📱 TELEGRAM: {message}")
        except Exception as e:
            print(f"❌ Telegram error: {e}")
    
    def send_trade_alert(self, trade_data):
        """Send trade alert"""
        symbol = trade_data['symbol']
        action = trade_data['action']
        price = trade_data['price']
        shares = trade_data['shares']
        value = trade_data['value']
        date = trade_data['date']
        
        message = f"🔔 TRADE ALERT\n📊 {symbol}\n🎯 {action} {shares} shares at ₹{price:.2f}\n💵 Total: ₹{value:,.0f}\n📅 {date}"
        self.send_message(message)
    
    def send_portfolio_summary(self, portfolio_data):
        """Send portfolio summary"""
        total_value = portfolio_data.get('total_value', 'N/A')
        avg_return = portfolio_data.get('average_return', 'N/A')
        best_performer = portfolio_data.get('best_performer', 'N/A')
        total_trades = portfolio_data.get('total_trades_executed', 'N/A')
        ml_accuracy = portfolio_data.get('average_ml_accuracy', 'N/A')
        
        message = f"💼 PORTFOLIO UPDATE\n💰 Total: {total_value}\n📊 Return: {avg_return}\n🏆 Best: {best_performer}\n📈 Trades: {total_trades}\n🤖 ML: {ml_accuracy}"
        self.send_message(message)
    
    def send_error_alert(self, error_message):
        """Send error notification"""
        message = f"⚠️ SYSTEM ERROR\n❌ {error_message}\nPlease check system logs."
        self.send_message(message)

# Test it
if __name__ == "__main__":
    BOT_TOKEN = "7657637482:AAF5Ar2OSmVsJPsbQUSPRyVhCf2oz2JULIc"
    
    telegram = TelegramAlert(BOT_TOKEN)
    
    telegram.send_trade_alert({
        'symbol': 'RELIANCE.NS',
        'action': 'BUY',
        'price': 1429.50,
        'shares': 20,
        'value': 28590,
        'date': '2025-08-07'
    })
    
    print("Telegram bot test completed!")