from aiogram import types
from aiogram.filters import BaseFilter


class FilterContact(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        if message.contact is not None:
            return True
        else:
            return False


class Filter:
    def __init__(self, message: types.Message) -> None:
        self.message = message


class FilterUserId(Filter):
    @staticmethod
    async def check_id(message: types.Message) -> bool:
        if message.from_user.id == message.contact.user_id:
            return True
        else:
            return False
