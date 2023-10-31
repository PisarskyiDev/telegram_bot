from typing import List

from aiogram import types
from aiogram.filters import BaseFilter

from bot.admin.core import list_commands


class FoundCommand(BaseFilter):
    @staticmethod
    async def __call__(message: types.Message) -> bool:
        commands = list_commands(functions=False)
        text = message.text.strip().lower().replace(" ", "_")
        return True if text in commands else False
