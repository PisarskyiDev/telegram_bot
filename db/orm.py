from __future__ import annotations

from typing import Type

from aiogram import types

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from db import models


async def register_user(
    message: types.Message, db: AsyncSession
) -> bool | str:
    username = (
        message.from_user.username if message.from_user.username else None
    )
    user = models.Users(
        id=int(message.from_user.id),
        username=username,
        name=message.from_user.full_name,
    )
    async with db.begin() as local_session:
        try:
            local_session.add(user)
            await local_session.commit()

            return True
        except IntegrityError as e:
            if "UniqueViolation" in str(e.args):
                return "Login was successful"
            else:
                await local_session.rollback()
                print(e)
                return False


async def select_user(user_id, db: AsyncSession) -> Type[models.Users]:
    async with db.begin() as local_session:
        return await local_session.get(models.Users, user_id)


async def save_message(message: types.Message, db: AsyncSession) -> None:
    db_message = models.Messages(
        id=message.message_id,
        message=message.text,
        user_id=message.from_user.id,
        chat_id=message.chat.id,
    )
    print(f"----------------------{message.chat.id}----------------------")

    async with db.begin() as local_session:
        try:
            chat = await select_chat(message=message, db=db)
            if chat:
                local_session.add(db_message)
                await local_session.commit()
        except Exception as e:
            await local_session.rollback()


async def select_chat(
    message: types.Message, db: AsyncSession
) -> Type[models.Chats] | bool:
    async with db.begin() as local_session:
        chat = await local_session.get(models.Chats, message.chat.id)
        if chat is not None:
            return chat
        if chat is None:
            chat = models.Chats(
                id=message.chat.id,
                type=message.chat.type,
                user_id=message.from_user.id,
            )
            local_session.add(chat)
            await local_session.commit()
            return True
        else:
            await local_session.rollback()
            return False
