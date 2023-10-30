from __future__ import annotations

import re

from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State

from bot.states.state import AllStates
from db.orm import update_user, select_user


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
        return
    try:
        target_user = re.findall(r"@(\w+)", message.text)
        if target_user:
            query_user = await select_user(user_id=message.from_user.id)
            target_user = await select_user(username=target_user[0])
            if target_user.admin and set_admin:
                await message.reply(
                    f"{target_user.username} - already admin",
                )
            if query_user.admin:
                query = {"admin": set_admin}
                response = await update_user(
                    user_id=target_user.id, data=query, message=message
                )
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
