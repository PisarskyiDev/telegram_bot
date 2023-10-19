from aiogram import Router, types

from api.open_ai.config import send_to_ai
from bot.buttons.keyboard import reset, profile
from bot.states.state import AllStates
from db.engine import session
from db.orm import save_message, get_last_message

ai = Router()


@ai.message(AllStates.logged_ai_on)
async def gpt_on_handler(message: types.Message) -> None:
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=profile + reset,
        resize_keyboard=True,
    )
    previous_massage = await get_last_message(message=message, db=session)
    try:
        await message.reply("Please wait a little bit, i`m thinking...")
        response_ai = await send_to_ai(
            question=message.text,
            previous_answer=previous_massage.answer
            if previous_massage
            else None,
            previous_question=previous_massage.question
            if previous_massage
            else None,
        )

        await message.answer(
            text=response_ai,
            reply_markup=keyboard,
        )
        await save_message(message=message, answer=response_ai, db=session)
    except TypeError as e:
        await message.answer("Nice try!")
