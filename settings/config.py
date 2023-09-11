import os
from dotenv import load_dotenv

load_dotenv()

TEST_HOST = os.getenv("TEST_HOST")
HOST = os.getenv("HOST")
HOST_API = os.getenv("HOST_API")
PORT = os.getenv("PORT")
LOCAL = os.getenv("LOCAL")

WEBHOOK_SECRET = os.getenv("SECRET")
TOKEN = os.getenv("TOKEN")

CALLBACK = os.getenv("CALLBACK")
WEBHOOK_PATH = "/webhook" + CALLBACK

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_USER = os.getenv("REDIS_USER")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")