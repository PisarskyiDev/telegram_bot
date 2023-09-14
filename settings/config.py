import os
from dotenv import load_dotenv

load_dotenv()

TEST_HOST = os.getenv("TEST_HOST")
HOST = os.getenv("HOST")
TELEGRAM_HOST = os.getenv("TELEGRAM_HOST")
LOGIN_URL = os.getenv("LOGIN_URL")
PORT = os.getenv("PORT")
LOCAL = os.getenv("LOCAL")

LOGIN = os.getenv("LOGIN")
PASSWORD = os.getenv("PASSWORD")

WEBHOOK_SECRET = os.getenv("SECRET")
TOKEN = os.getenv("TOKEN")

CALLBACK = os.getenv("CALLBACK")
WEBHOOK_PATH = "/webhook" + CALLBACK

TOKEN_URL = os.getenv("TOKEN_URL")
REGISTRATE_URL = os.getenv("REGISTRATE_URL")

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_USER = os.getenv("REDIS_USER")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

GPT_KEY = os.getenv("GPT_KEY")
