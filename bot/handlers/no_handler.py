from aiogram import Router, types

from bot.buttons import keyboard
from bot.states.state import AllStates

no_handler = Router()


@no_handler.message(AllStates.no_login)
async def echo_handler(message: types.Message) -> None:
    kb = keyboard.start_kb

    try:
        await message.answer(
            "To use this bot you need to SHARE your number on it first",
            reply_markup=kb,
        )
    except TypeError:
        await message.answer("Nice try!")
