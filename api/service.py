import random
import string
import aiohttp
import json

from typing import Any

from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.fsm.storage.base import StorageKey


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


async def redis_data(
    state: FSMContext,
    message: Message,
    data: dict[str, Any] = None,
):
    if data is None:
        from_redis = await state.storage.get_data(
            key=StorageKey(
                bot_id=message.bot.id,
                user_id=message.from_user.id,
                chat_id=message.chat.id,
            )
        )
    else:
        from_redis = await state.storage.set_data(
            key=StorageKey(
                bot_id=message.bot.id,
                user_id=message.from_user.id,
                chat_id=message.chat.id,
            ),
            data=data,
        )
    return from_redis


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
