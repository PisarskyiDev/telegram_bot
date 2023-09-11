import os
from dotenv import load_dotenv

load_dotenv()

TEST_HOST = os.getenv("TEST_HOST")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
LOCAL = os.getenv("LOCAL")

WEBHOOK_SECRET = os.getenv("SECRET")
TOKEN = os.getenv("TOKEN")

CALLBACK = os.getenv("CALLBACK")
WEBHOOK_PATH = "/webhook" + CALLBACK
