from datetime import time, datetime

from aiogram import Router, types, html, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from bot.buttons.keyboard import (
    reset,
    keyboard_build,
)
from bot.filter.contact import FilterContact, FilterUserId
from bot.states.state import AllStates
from db.orm import register_user

checkout = Router()


@checkout.message(FilterContact())
async def login_handler(message: Message, state: FSMContext) -> None:
    keyboard = keyboard_build(reset)
    check = await FilterUserId.check_id(message)

    if not check:
        await message.reply(
            "Номер не подтвержден! Вы не можете использовать чужой номер!",
            reply_markup=keyboard,
        )
        await state.set_state(AllStates.no_login)
    else:
        start_time = datetime.now()  # start time, DOWT LEFT IN PROD

        user = await register_user(message)

        end_time = datetime.now()  # start time, DOWT LEFT IN PROD
        time_difference = (
            end_time - start_time
        ).total_seconds()  # start time, DOWT LEFT IN PROD
        await message.reply(str(time_difference))
        if user and isinstance(user, str):
            await message.reply(user, reply_markup=keyboard)
        elif user:
            await message.reply(
                "Number confirmed successfully! Your account was created!",
                reply_markup=keyboard,
            )
            await message.reply(
                "Now you can use this bot!", reply_markup=keyboard
            )
        else:
            await message.reply(
                (
                    "Number confirmed successfully! But your account was not created!"
                    "Please try again"
                ),
                reply_markup=keyboard,
            )
        await state.set_state(AllStates.logged_ai_on)
