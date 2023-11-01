from aiogram import types
from aiogram.filters import BaseFilter

from db.orm import UserORM


class Admin(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        user = await UserORM().select_user(user_id=message.from_user.id)
        return user.admin


class NoAdmin(Admin):
    async def __call__(self, message: types.Message) -> bool:
        user = await UserORM().select_user(user_id=message.from_user.id)
        return not user.admin
