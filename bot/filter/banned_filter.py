from aiogram import types
from aiogram.filters import BaseFilter

from db.orm import UserORM


class Banned(BaseFilter):
    async def __call__(self, message: types.Message) -> bool | None:
        user = None
        if user is None or message.from_user.id != user.id:
            user = await UserORM().select_user(user_id=message.from_user.id)

        if user.banned:
            return True
        elif not user.banned:
            return False
        else:
            return None
