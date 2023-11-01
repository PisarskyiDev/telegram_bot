from __future__ import annotations

import re

from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State

from bot.states.state import AllStates
from db import models

from db.orm import UserORM


async def manage_admin(
    message: types.Message,
    text: str = "Enter username",
    state: FSMContext = None,
    state_type: State = None,
    ai: bool = False,
    set_admin: bool = True,
) -> bool | None:
    response = None
    if ai:
        await state.set_state(state_type)
        await message.reply(text)

    try:
        target_user = get_username_from_message(message)
        if target_user:
            query_user = await UserORM().select_user(
                user_id=message.from_user.id
            )
            target_user = await UserORM().select_user(username=target_user)

            if target_user.admin and set_admin:
                await message.reply(
                    f"@{target_user.username} - already admin",
                )
                response = True
                return
            elif not target_user.admin and not set_admin:
                await message.reply(
                    f"@{query_user.username} - not admin",
                )
                response = True
                return

            if target_user.admin and set_admin:
                await message.reply(
                    f"{target_user.username} - already admin",
                )

            if query_user.admin:
                query = {"admin": set_admin}
                response = await UserORM(
                    model=models.Users, message=message
                ).update(user_id=target_user.id, data=query)

            await message.reply(
                f"{message.text} - "
                f"{'is' if set_admin else 'is not'} admin now",
            )
            await state.set_state(AllStates.login)

            response = True
    except Exception as e:
        await state.set_state(AllStates.login)
    finally:
        return response


def get_username_from_message(message: types.Message) -> str:
    username = re.findall(r"@(.+)", message.text)[0]
    return username
