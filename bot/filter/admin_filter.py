from aiogram import types
from aiogram.filters import BaseFilter

from db.orm import UserORM

USER = None


class Admin(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        global USER
        if USER is None or message.from_user.id != USER.id:
            USER = await UserORM().select_user(user_id=message.from_user.id)
        return USER.admin


class NoAdmin(Admin):
    async def __call__(self, message: types.Message) -> bool:
        global USER
        if USER is None or message.from_user.id != USER.id:
            USER = await UserORM().select_user(user_id=message.from_user.id)
        return not USER.admin
