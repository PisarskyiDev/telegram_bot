import configparser
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


BOT_DB_USERNAME = os.getenv("BOT_DB_USERNAME")
BOT_DB_PASSWORD = os.getenv("BOT_DB_PASSWORD")
BOT_DB_URL = os.getenv("BOT_DB_URL")
BOT_DB_NAME = os.getenv("BOT_DB_NAME")
