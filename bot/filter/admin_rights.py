from aiogram import types
from aiogram.filters import BaseFilter

from db.engine import session
from db.orm import select_user


class AdminRights(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        user = await select_user(user_id=message.from_user.id, db=session)
        if user.admin:
            return True
        else:
            return False
