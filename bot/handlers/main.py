from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.buttons.keyboard import start, reset, login, registration
from bot.buttons.keyboard import keyboard_build
from bot.states.state import AllStates

main = Router()


@main.message(F.text.lower() == "reset")
async def reset_handler(message: Message, state: FSMContext) -> None:
    keyboard = keyboard_build(start + reset)

    await message.answer(
        "Reset was successful!",
        reply_markup=keyboard,
    )

    await state.clear()


@main.message(F.text.lower() == "start")
async def start_handler(message: Message, state: FSMContext) -> None:
    keyboard = keyboard_build(registration + reset + login)

    await message.answer(
        "To use this bot you need to register on it first. Were you want to do it?",
        reply_markup=keyboard,
    )
    await state.set_state(AllStates.no_login)
