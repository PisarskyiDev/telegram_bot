from __future__ import annotations

import re

from aiogram import types
from aiogram.fsm.context import FSMContext
from bot.buttons import keyboard
from bot.states.state import AllStates
from db.orm import select_user, update_user


class Commands:
    @staticmethod
    async def battery_power(
        message: types.Message, _state: FSMContext
    ) -> None:
        await message.reply("Done! Battery is on!")

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
    async def make_admin(
        message: types.Message, state: FSMContext, ai: bool = False
    ) -> bool | None:
        if not ai:
            target_users = re.findall(r"@(\w+)", message.text)[0].split(",")
            response = None

            user = await select_user(username=target_users[0])
            if user and user.admin:
                await message.reply(
                    "You already have admin rights",
                    reply_markup=keyboard.admin_on_kb,
                )
                response = False

            elif user and not user.admin:
                response = await update_user(
                    user_id=user.id,
                    data={"admin": True},
                    message=message,
                )
                await message.reply(
                    f"{message.from_user.username} - have admin rights now",
                )
            return response
        else:
            await state.set_state(AllStates.waiting_for_username)
            await message.reply("Send username to GIVE him admin rights")

    @staticmethod
    def del_admin():
        pass

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
