from aiogram import Router, types

from api.open_ai.config import send_to_ai
from bot.buttons.keyboard import reset, profile
from bot.states.state import AllStates
from db.engine import session
from db.orm import save_message

ai = Router()


@ai.message(AllStates.logged_ai_on)
async def gpt_on_handler(message: types.Message) -> None:
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=profile + reset,
        resize_keyboard=True,
    )
    try:
        await message.reply("Please wait a little bit, i`m thinking...")
        response_ai = await send_to_ai(message.text)

        await message.answer(
            text=response_ai,
            reply_markup=keyboard,
        )
        await save_message(message=message, answer=response_ai, db=session)
    except TypeError as e:
        await message.answer("Nice try!")
        print(e)
