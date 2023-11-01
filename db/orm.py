from __future__ import annotations

from typing import Type, Any

from aiogram import types
from sqlalchemy import select

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from db import models
from db.engine import session


class UserORM:
    def __init__(
        self,
        model: models = models.Users,
        message: types.Message = None,
        schedule: models = models.Schedule,
    ):
        self.model = model
        self.schedule = schedule
        self.db = session
        self.message = message

    async def update(
        self,
        user_id: int,
        data: dict[str, Any],
    ) -> bool | None:
        async with self.db.begin() as local_session:
            try:
                # user = await local_session.get(self.model, user_id)
                query = select(self.model).filter(
                    self.model.user_id == user_id
                )
                query_instance = await local_session.execute(query)
                schedule = query_instance.scalars().first()
                if schedule:
                    for key, value in data.items():
                        if hasattr(schedule, key):
                            setattr(schedule, key, value)
                    await local_session.commit()
                    await local_session.close()
                    return True
            except Exception:
                await local_session.rollback()
                await local_session.close()
                await self.message.answer(
                    "Something went wrong, please contact to admin",
                )
                return False

    async def register(
        self,
    ) -> bool | str:
        result = None
        username = (
            self.message.from_user.username
            if self.message.from_user.username
            else None
        )

        async with self.db.begin() as local_session:
            try:
                if self.model is models.Users:
                    user = self.model(
                        id=self.message.from_user.id,
                        username=username,
                        name=self.message.from_user.full_name,
                        phone=self.message.contact.phone_number,
                    )
                    schedule = self.schedule(
                        user_id=user.id, user=user, active=False
                    )
                    local_session.add(user)
                    local_session.add(schedule)
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

    async def get_all_users(self) -> list[Type[models.Users]]:
        async with self.db.begin() as local_session:
            query = select(self.model)
            query_instance = await local_session.execute(query)
            users = query_instance.scalars().unique().all()
            await local_session.close()
            return users

    async def select_user(
        self,
        user_id: int = None,
        username: str = None,
    ) -> Type[models.Users] | None:
        async with self.db.begin() as local_session:
            if user_id is not None:
                user = await local_session.get(models.Users, user_id)
                await local_session.close()
            elif username is not None:
                query = select(self.model).filter(
                    self.model.username == str(username)
                )
                query_instance = await local_session.execute(query)
                user = query_instance.scalar()
                await local_session.close()

            else:
                return None
            return user


class MessageORM:
    def __init__(
        self,
        model: models = models.Messages,
        message: types.Message = None,
    ):
        self.model = model
        self.db = session
        self.message = message

    async def save_message(self, response_ai: str) -> None:
        db_message = models.Messages(
            id=self.message.message_id,
            question=self.message.text,
            answer=response_ai,
            user_id=self.message.from_user.id,
            chat_id=self.message.chat.id,
        )

        async with self.db.begin() as local_session:
            try:
                chat = await ChatORM(message=self.message).select_chat()

                if chat:
                    local_session.add(db_message)
                    await local_session.commit()
            except Exception:
                await local_session.rollback()
            finally:
                await local_session.close()

    async def get_last_message(self) -> Type[models.Messages] | bool:
        result = False
        try:
            async with self.db.begin() as local_session:
                query = (
                    select(models.Messages)
                    .filter(self.model.user_id == self.message.from_user.id)
                    .order_by(models.Messages.id.desc())
                    .limit(1)
                )
                query_instance = await local_session.execute(query)
                user = query_instance.scalar()

                result = user
        except Exception:
            await local_session.rollback()
        finally:
            await local_session.close()
            return result


class ChatORM:
    def __init__(
        self,
        model: models = models.Chats,
        message: types.Message = None,
        schedule: models = models.Schedule,
    ):
        self.model = model
        self.schedule = schedule
        self.db = session
        self.message = message

    async def select_chat(self) -> Type[models.Chats] | bool:
        async with self.db.begin() as local_session:
            result = None
            chat = await local_session.get(self.model, self.message.chat.id)
            if chat is not None:
                result = chat

            elif chat is None:
                chat = models.Chats(
                    id=self.message.chat.id,
                    type=self.message.chat.type,
                    user_id=self.message.from_user.id,
                )
                local_session.add(chat)
                await local_session.commit()
                result = True

            else:
                await local_session.rollback()
                result = False
            await local_session.close()
            return result


class ScheduleORM:
    def __init__(
        self,
        model: models = models.Schedule,
        message: types.Message = None,
    ):
        self.model = model
        self.db = session
        self.message = message

    async def get_schedule_users(self) -> None:
        async with self.db.begin() as local_session:
            query = select(self.model.user_id).filter(
                self.model.active == True
            )
            query_instance = await local_session.execute(query)
            users = query_instance.scalars().unique().all()
            await local_session.close()
            return users

    async def set_schedule(
        self, target_id: int, activate: bool = True
    ) -> bool:
        try:
            user = await UserORM(model=self.model).update(
                user_id=target_id, data={"active": activate}
            )
            return True
        except Exception:
            return False
