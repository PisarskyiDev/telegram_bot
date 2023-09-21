from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.buttons.keyboard import reset
from bot.states.state import AllStates

registration = Router()


@registration.message(AllStates.confirm_email, F.text.lower() == "edit")
async def edit_email_handler(message: Message, state: FSMContext) -> None:
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=reset,
    )
    await message.answer(
        text="Enter your new email:",
        reply_markup=keyboard,
    )
    await state.set_state(AllStates.enter_email)


@registration.message(AllStates.no_login, F.text.lower() == "here")
async def here_handler(message: Message, state: FSMContext) -> None:
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=reset,
        resize_keyboard=True,
    )
    await message.answer(
        text="Enter your email:",
        reply_markup=keyboard,
    )

    await state.set_state(AllStates.enter_email)
