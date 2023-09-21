from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from api.open_ai.config import send_to_ai
from bot.buttons.keyboard import ai_on, ai_off, reset
from bot.states.state import AllStates

ai = Router()


@ai.message(F.text.lower() == "ai on", AllStates.logged_ai_off)
async def gpt_on_handler(message: Message, state: FSMContext) -> None:
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=ai_off + reset,
        resize_keyboard=True,
        input_field_placeholder="Ai off?",
    )
    await message.answer("Ai is on", reply_markup=keyboard)
    await state.set_state(AllStates.logged_ai_on)


@ai.message(F.text.lower() == "ai off", AllStates.logged_ai_on)
async def echo_gpt_off_handler(message: Message, state: FSMContext) -> None:
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=ai_on + reset,
        resize_keyboard=True,
        input_field_placeholder="Ai On?",
    )
    await message.answer("Ai is off", reply_markup=keyboard)
    await state.set_state(AllStates.logged_ai_off)


@ai.message(AllStates.logged_ai_on)
async def echo_gpt_on_handler(message: types.Message) -> None:
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=ai_off + reset,
        resize_keyboard=True,
    )
    try:
        response_ai = await send_to_ai(message.text)
        await message.answer(
            text=response_ai,
            reply_markup=keyboard,
        )
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")
