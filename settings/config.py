import os
from dotenv import load_dotenv

load_dotenv()


# Get datas from .env
HOST = os.getenv("HOST")

LOGIN_URL = os.getenv("LOGIN_URL")
PORT = os.getenv("PORT")
LOCAL = os.getenv("LOCAL")

LOGIN = os.getenv("LOGIN")
PASSWORD = os.getenv("PASSWORD")

# Telegram
# TEST_TOKEN = os.getenv("TEST_TOKEN")
WEBHOOK_SECRET = os.getenv("SECRET")
TOKEN = os.getenv("TOKEN")


CALLBACK = os.getenv("CALLBACK")
WEBHOOK_PATH = "/webhook" + CALLBACK

# Django
TOKEN_URL = os.getenv("TOKEN_URL")
REGISTRATE_URL = os.getenv("REGISTRATE_URL")

# Redis
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_USER = os.getenv("REDIS_USER")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

# AI
GPT_KEY = os.getenv("GPT_KEY")

# HomeAssistant
HA_TOKEN = os.getenv("HA_TOKEN")
HA_LINK = os.getenv("HA_LINK")

# PostgreSQL
BOT_DB_USERNAME = os.getenv("BOT_DB_USERNAME")
BOT_DB_PASSWORD = os.getenv("BOT_DB_PASSWORD")
BOT_DB_URL = os.getenv("BOT_DB_URL")
BOT_DB_NAME = os.getenv("BOT_DB_NAME")
