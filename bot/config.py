import os
from dotenv import load_dotenv

load_dotenv()

# Telegram
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME")

# OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")

# Image Generation
IMAGE_API_URL = os.getenv("IMAGE_API_URL", "https://api.mymidjourney.ai/api/v1/midjourney")
IMAGE_API_KEY = os.getenv("IMAGE_API_KEY")

# Settings
TIMEZONE = os.getenv("TIMEZONE", "Europe/Moscow")
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", 30))
STATE_FILE = "state.json"

# Posting times
POSTING_TIMES = [
    "08:00", "10:00", "12:00", "14:00", 
    "16:00", "18:00", "20:00", "22:00"
]
