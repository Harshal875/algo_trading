"""
Windows-Friendly Logger for Algo Trading System
Handles Unicode issues on Windows console
"""
import logging
import logging.handlers
import os
from datetime import datetime
from pathlib import Path
import sys

class TradingLogger:
    """Windows-friendly logger for the trading system"""
    
    def __init__(self, name=__name__, log_level="INFO", log_dir="logs"):
        self.name = name
        self.log_level = getattr(logging, log_level.upper())
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Initialize logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(self.log_level)
        
        # Prevent duplicate handlers
        if self.logger.handlers:
            self.logger.handlers.clear()
        
        self._setup_handlers()
    
    def _setup_handlers(self):
        """Setup file and console handlers with proper encoding"""
        # Create formatters
        detailed_formatter = logging.Formatter(
            '%(asctime)s | %(name)s | %(levelname)s | %(funcName)s:%(lineno)d | %(message)s'
        )
        
        simple_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)s | %(message)s'
        )
        
        # File handler with UTF-8 encoding (for emojis in files)
        file_handler = logging.handlers.RotatingFileHandler(
            self.log_dir / f"trading_system_{datetime.now().strftime('%Y%m%d')}.log",
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding='utf-8'  # Important for Windows
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(detailed_formatter)
        
        # Console handler with error handling for Windows
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(self.log_level)
        console_handler.setFormatter(simple_formatter)
        
        # Error file handler with UTF-8 encoding
        error_handler = logging.FileHandler(
            self.log_dir / f"errors_{datetime.now().strftime('%Y%m%d')}.log",
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(detailed_formatter)
        
        # Add handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        self.logger.addHandler(error_handler)
    
    def get_logger(self):
        """Get the configured logger instance"""
        return self.logger
    
    # Convenience methods with safe Unicode handling
    def _safe_message(self, message):
        """Convert emojis to safe characters for Windows console"""
        if isinstance(message, str):
            # Replace common emojis with text equivalents for console
            replacements = {
                '🚀': '[START]',
                '📊': '[DATA]',
                '📈': '[UP]',
                '📉': '[DOWN]',
                '🤖': '[ML]',
                '💰': '[MONEY]',
                '✅': '[OK]',
                '❌': '[ERROR]',
                '⚠️': '[WARN]',
                '🏆': '[WIN]',
                '📱': '[MSG]',
                '🔍': '[SEARCH]',
                '₹': 'Rs'
            }
            
            safe_message = message
            for emoji, replacement in replacements.items():
                safe_message = safe_message.replace(emoji, replacement)
            return safe_message
        return message
    
    def info(self, message):
        try:
            self.logger.info(message)
        except UnicodeEncodeError:
            # Fallback to safe message
            self.logger.info(self._safe_message(message))
    
    def debug(self, message):
        try:
            self.logger.debug(message)
        except UnicodeEncodeError:
            self.logger.debug(self._safe_message(message))
    
    def warning(self, message):
        try:
            self.logger.warning(message)
        except UnicodeEncodeError:
            self.logger.warning(self._safe_message(message))
    
    def error(self, message):
        try:
            self.logger.error(message)
        except UnicodeEncodeError:
            self.logger.error(self._safe_message(message))
    
    def critical(self, message):
        try:
            self.logger.critical(message)
        except UnicodeEncodeError:
            self.logger.critical(self._safe_message(message))

# Global logger instance
def get_logger(name=__name__, log_level="INFO"):
    """Get a logger instance for any module"""
    return TradingLogger(name, log_level).get_logger()

# Test the logger
if __name__ == "__main__":
    # Test Windows-friendly logging
    logger = TradingLogger(__name__, "INFO")
    
    logger.info("Testing Windows-friendly logger")
    logger.info("System initialized successfully")
    logger.info("Data analysis complete - Return: +2.5%")
    logger.info("All components working!")
    
    print("Windows-friendly logger test completed - check logs/ directory")