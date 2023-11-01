from typing import Any

from aiogram import types, Bot
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext

from bot.admin.manage import manage_admin, get_username_from_message
from bot.buttons import keyboard
from bot.states.state import AllStates
from db.orm import UserORM, ScheduleORM
from requests import get, ReadTimeout

from settings.config import HA_TOKEN, TOKEN
from settings.config import HA_LINK


class Commands:
    @staticmethod
    async def battery_power(
        message: types.Message = None,
        _state: FSMContext = None,
        _ai: bool = None,
    ) -> Any:
        url = f"https://{HA_LINK}/api/states/sensor.jk_b2a24s15p_battery1_voltage"
        headers = {
            "Authorization": f"Bearer {HA_TOKEN}",
            "content-type": "application/json",
        }
        try:
            response = get(url, headers=headers, timeout=3)
        except ReadTimeout:
            response = "unavailable"

        if response != "unavailable":
            state = response.json()["state"]
            current_voltage = float(state)
            min_voltage = 42.00
            max_voltage = 58.80
            percent = str(
                int(
                    (
                        (current_voltage - min_voltage)
                        / (max_voltage - min_voltage)
                    )
                    * 100
                )
            )

            if message is not None:
                await message.reply(
                    "Уровень заряда: "
                    + percent
                    + "%"
                    + f"\nНапряжение батарей: {current_voltage}V",
                    reply_markup=keyboard.default_kb,
                )
            else:
                if response.status_code == 200:
                    return [current_voltage, percent]
        return response

    @staticmethod
    async def add_admin(
        message: types.Message, state: FSMContext, ai: bool = False
    ) -> bool | None:
        return await manage_admin(
            message=message,
            state=state,
            ai=ai,
            set_admin=True,
        )

    @staticmethod
    async def del_admin(
        message: types.Message, state: FSMContext, ai: bool = False
    ) -> bool | None:
        result = await manage_admin(
            message=message,
            state=state,
            ai=ai,
            set_admin=False,
        )
        return result

    @staticmethod
    def ban_user():
        pass

    @staticmethod
    def unban_user():
        pass

    @staticmethod
    async def all_users(
        message: types.Message, state: FSMContext, _ai: bool = False
    ) -> None:
        users = await UserORM().get_all_users()
        bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
        for user in users:
            await bot.send_message(
                chat_id=message.from_user.id,
                text=f"@{user.username} - {user.id}",
            )
            await state.set_state(AllStates.login)

    @staticmethod
    async def change_schedule(
        message: types.Message,
        activate: bool,
        _state: FSMContext = None,
        _ai: bool = False,
    ) -> bool | None:
        target_user = get_username_from_message(message)
        user = await UserORM().select_user(username=target_user)

        if user is not None:
            response = await ScheduleORM(message=message).set_schedule(
                target_id=user.id,
                activate=activate,
            )
            return response

    @staticmethod
    def user_commands_list():
        pass
