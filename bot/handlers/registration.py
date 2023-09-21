from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.buttons.keyboard import reset, keyboard_build
from bot.states.state import AllStates

registration = Router()


@registration.message(AllStates.confirm_email, F.text.lower() == "edit")
async def edit_email_handler(message: Message, state: FSMContext) -> None:
    keyboard = keyboard_build(reset, placeholder="Enter your new email")

    await message.answer(
        text="Enter your new email:",
        reply_markup=keyboard,
    )
    await state.set_state(AllStates.enter_email)


@registration.message(AllStates.no_login, F.text.lower() == "here")
async def here_handler(message: Message, state: FSMContext) -> None:
    keyboard = keyboard_build(reset, placeholder="Enter your new email")

    await message.answer(
        text="Enter your email:",
        reply_markup=keyboard,
    )

    await state.set_state(AllStates.enter_email)
