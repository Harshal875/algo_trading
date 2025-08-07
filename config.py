"""
Simple Configuration - Just load environment variables
"""
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Get environment variables (with defaults)
GOOGLE_SHEET_URL = os.getenv("GOOGLE_SHEET_URL", "")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# That's it! Keep it simple.
print(f"✅ Config loaded - Log level: {LOG_LEVEL}")