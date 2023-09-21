from aiogram import Router, types

from bot.buttons.keyboard import registration, reset, login, keyboard_build
from bot.states.state import AllStates

no_handler = Router()


@no_handler.message(
    AllStates.no_login,
    AllStates.check_login,
    AllStates.registration,
    AllStates.enter_email,
    AllStates.error,
    AllStates.start,
)
@no_handler.message()
async def echo_handler(message: types.Message) -> None:
    keyboard = keyboard_build(registration + login + reset)

    try:
        await message.answer(
            "You should registrate or login first!",
            reply_markup=keyboard,
        )
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")
