from __future__ import annotations

from typing import Type, Any

from aiogram import types
from sqlalchemy import select

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from db import models
from db.engine import session


async def register_user(
    message: types.Message,
    db: Session = session,
) -> bool | str:
    result = None
    username = (
        message.from_user.username if message.from_user.username else None
    )

    async with db.begin() as local_session:
        try:
            user = models.Users(
                id=message.from_user.id,
                username=username,
                name=message.from_user.full_name,
                phone=message.contact.phone_number,
            )
            local_session.add(user)
            await local_session.commit()
            result = True
        except IntegrityError as e:
            if "UniqueViolation" in str(e.args):
                result = "Login was successful"
            else:
                await local_session.rollback()
                result = False
        finally:
            await local_session.close()
            return result


async def sql_all_users(db: Session = session) -> list[Type[models.Users]]:
    async with db.begin() as local_session:
        query = select(models.Users)
        query_instance = await local_session.execute(query)
        users = query_instance.scalars().unique().all()
        await local_session.close()
        return users


async def select_user(
    user_id: int = None,
    username: str = None,
    db: Session = session,
) -> Type[models.Users] | None:
    async with db.begin() as local_session:
        if user_id is not None:
            user = await local_session.get(models.Users, user_id)
            await local_session.close()
        elif username is not None:
            query = select(models.Users).filter(
                models.Users.username == str(username)
            )
            query_instance = await local_session.execute(query)
            user = query_instance.scalar()
            await local_session.close()
        else:
            return None
        return user


async def update_user(
    user_id: int,
    data: dict[str, Any],
    message: types.Message,
    db: Session = session,
) -> bool | None:
    async with db.begin() as local_session:
        try:
            user = await local_session.get(models.Users, user_id)
            if user:
                for key, value in data.items():
                    if hasattr(user, key):
                        setattr(user, key, value)
                await local_session.commit()
                await local_session.close()
                return True
        except Exception as e:
            await local_session.rollback()
            await local_session.close()
            await message.answer(
                "Something went wrong, please contact to admin",
            )
            return False


async def save_message(
    message: types.Message,
    answer: str,
    db: Session = session,
) -> None:
    db_message = models.Messages(
        id=message.message_id,
        question=message.text,
        answer=answer,
        user_id=message.from_user.id,
        chat_id=message.chat.id,
    )

    async with db.begin() as local_session:
        try:
            chat = await select_chat(message=message, db=db)

            if chat:
                local_session.add(db_message)
                await local_session.commit()
        except Exception as e:
            await local_session.rollback()
        finally:
            await local_session.close()


async def get_last_message(
    message: types.Message, db: Session
) -> Type[models.Messages] | bool:
    result = False
    try:
        async with db.begin() as local_session:
            query = (
                select(models.Messages)
                .filter(models.Messages.user_id == message.from_user.id)
                .order_by(models.Messages.id.desc())
                .limit(1)
            )
            query_instance = await local_session.execute(query)
            user = query_instance.scalar()

            result = user
    except Exception as e:
        await local_session.rollback()
    finally:
        await local_session.close()
        return result


async def select_chat(
    message: types.Message, db: Session
) -> Type[models.Chats] | bool:
    async with db.begin() as local_session:
        result = None
        chat = await local_session.get(models.Chats, message.chat.id)
        if chat is not None:
            result = chat

        elif chat is None:
            chat = models.Chats(
                id=message.chat.id,
                type=message.chat.type,
                user_id=message.from_user.id,
            )
            local_session.add(chat)
            await local_session.commit()
            result = True

        else:
            await local_session.rollback()
            result = False
        await local_session.close()
        return result
