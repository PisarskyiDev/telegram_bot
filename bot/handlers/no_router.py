from aiogram import Router, types

from bot.commands.buttons import registration, cancel, login
from bot.filters.states import Form as States

no_handler = Router()


@no_handler.message(
    States.no_login,
    States.check_login,
    States.registration,
    States.enter_email,
    States.error,
    States.before_finish,
    States.before_finish,
    States.start,
)
@no_handler.message()
async def echo_handler(message: types.Message) -> None:
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=registration + login + cancel,
    )
    try:
        await message.answer(
            "You should registrate or login first!",
            reply_markup=keyboard,
        )
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")
