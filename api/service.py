import random
import re
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
                return {
                    "response": response.status
                }  # TODO add handler if user exist or problem with data


def get_clear_data(
    message: Message, password: bool = False, url: bool = False
) -> dict:
    data = {}
    data["email"] = ""
    if url:
        data["URL"] = ""
    entities = message.entities
    for item in entities:
        for item.type in data.keys():
            data[item.type] = item.extract_from(message.text)
    if password:
        text = re.search(r"\((.*?)\)", message.text)
        text = text.group(1)
        data["password"] = text
    return data


def generate_password():
    tsk = "tsk"
    uppercase_letter = random.choice(string.ascii_uppercase)
    lowercase_letters = "".join(
        random.choice(string.ascii_lowercase) for _ in range(3)
    )
    digits = "".join(random.choice(string.digits) for _ in range(4))
    symbols = "".join(random.choice(string.punctuation))

    password = (
        tsk + uppercase_letter + lowercase_letters + digits + symbols + "!"
    )

    return password
