import random
import string

from aiogram.types import Message

import aiohttp
import json


async def send_request_to_api(email, password, url, token=False):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "" if not token else f"Bearer {token}",
    }
    data = {
        "email": email,
        "password": password,
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(
            url,
            headers=headers,
            data=json.dumps(data),
        ) as response:
            if response.status == 200:
                response_data = await response.json()
                return {
                    "response": response.status,
                    "access": response_data.get("access"),
                    "refresh": response_data.get("refresh"),
                }
            else:
                message = await response.text()
                return message


def get_clear_data(message: Message) -> dict:
    data = {
        # "URL": "",
        "email": "",
        # "password": "",
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
