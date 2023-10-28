from __future__ import annotations

from aiogram import types
from aiogram.fsm.context import FSMContext

from bot.admin.manage import manage_admin
from bot.buttons import keyboard
from bot.states.state import AllStates
from db.orm import select_user
from requests import get

from settings.config import HA_TOKEN
from settings.config import HA_LINK


class Commands:
    @staticmethod
    async def battery_power(
        message: types.Message, _state: FSMContext
    ) -> None:
        url = f"https://{HA_LINK}/api/states/sensor.jk_b2a24s15p_battery1_voltage"
        headers = {
            "Authorization": f"Bearer {HA_TOKEN}",
            "content-type": "application/json",
        }

        response = get(url, headers=headers)
        state = response.json()["state"]
        await message.reply(state)

    @staticmethod
    async def admin_mode(
        message: types.Message,
        state: FSMContext,
        ai: bool = False,
    ) -> None:
        is_admin = await select_user(user_id=message.from_user.id)
        exist_state = await state.get_state()

        if exist_state == AllStates.login and is_admin.admin:
            await state.set_state(AllStates.admin_mode)
            admin_on_kb = keyboard.admin_on_kb
            await message.reply(
                "Admin mode is activated!", reply_markup=admin_on_kb
            )
            await state.set_state(AllStates.admin_mode)

        elif exist_state == AllStates.admin_mode:
            admin_off_kb = keyboard.default_kb
            await message.reply(
                "Admin mode is deactivated!", reply_markup=admin_off_kb
            )
            await state.set_state(AllStates.login)
        else:
            await message.reply(
                "You dont have admin rights",
                reply_markup=keyboard.default_kb,
            )

    @staticmethod
    async def give_admin(
        message: types.Message, state: FSMContext, ai: bool = False
    ) -> bool | None:
        state_type = AllStates.waiting_for_give
        return await manage_admin(
            message=message,
            state=state,
            state_type=state_type,
            ai=ai,
            set_admin=True,
        )

    @staticmethod
    async def take_admin(
        message: types.Message, state: FSMContext, ai: bool = False
    ) -> bool | None:
        state_type = AllStates.waiting_for_take
        return await manage_admin(
            message=message,
            state=state,
            state_type=state_type,
            ai=ai,
            set_admin=False,
        )

    @staticmethod
    def ban_user():
        pass

    @staticmethod
    def unban_user():
        pass

    @staticmethod
    def users_list():
        pass

    @staticmethod
    def user_commands_list():
        pass


# variables = globals()
