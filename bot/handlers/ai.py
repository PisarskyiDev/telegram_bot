from aiogram import Router, types

from api.open_ai.config import send_to_ai
from bot.buttons.keyboard import reset
from bot.states.state import AllStates

ai = Router()


@ai.message(AllStates.logged_ai_on)
async def echo_gpt_on_handler(message: types.Message) -> None:
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=reset,
        resize_keyboard=True,
    )
    try:
        response_ai = await send_to_ai(message.text)
        await message.answer(
            text=response_ai,
            reply_markup=keyboard,
        )
    except TypeError:
        await message.answer("Nice try!")
