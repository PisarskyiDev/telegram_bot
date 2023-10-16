from aiogram import Router, types

from bot.buttons.keyboard import reset, share, keyboard_build
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
    keyboard = keyboard_build(reset + share)

    try:
        await message.answer(
            "To use this bot you need to SHARE your number on it first",
            reply_markup=keyboard,
        )
    except TypeError:
        await message.answer("Nice try!")
