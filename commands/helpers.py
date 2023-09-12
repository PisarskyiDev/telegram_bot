import json
import random
import string
import aiohttp

from aiogram.types import Message

from settings.config import TOKEN_URL, REGISTRATE_URL


def get_clear_data(message: Message) -> dict:
    data = {
        "URL": "",
        "email": "",
        "password": "",
    }
    entities = message.entities
    for item in entities:
        for item.type in data.keys():
            data[item.type] = item.extract_from(message.text)

    return data


def generate_password(length=15):
    characters = string.ascii_letters + string.digits + string.punctuation

    password = "".join(random.choice(characters) for _ in range(length))

    return password


async def get_admin_token(email, password):
    async with aiohttp.ClientSession() as session:
        headers = {
            "Content-Type": "application/json",
            "Authorization": "",
        }

        url = TOKEN_URL
        data = {
            "email": email,
            "password": password,
        }
        async with session.post(
            url,
            headers=headers,
            data=json.dumps(data),
        ) as response:
            if response.status == 200:
                data = await response.json()
                return data["access"]
            else:
                error = await response.text()
                print("Ошибка:", response.status)
                print("Текст ошибки:", error)
                return error


async def post_registrate_telegram_user(email, password, token):
    async with aiohttp.ClientSession() as session:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }
        url = REGISTRATE_URL
        data = {
            "email": email,
            "password": password,
        }
        async with session.post(
            url,
            headers=headers,
            data=json.dumps(data),
        ) as response:
            if response.status == 200:
                data = await response.json()
                return data.text()
            else:
                error = await response.text()
                print("Ошибка:", response.status)
                print("Текст ошибки:", error)
                return error
