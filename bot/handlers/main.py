from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.buttons.keyboard import start, reset, share
from bot.buttons.keyboard import keyboard_build
from bot.states.state import AllStates

main = Router()


@main.message(F.text.lower() == "reset")
@main.message(Command("reset"))
async def reset_handler(message: Message, state: FSMContext) -> None:
    keyboard = keyboard_build(start + reset)

    await message.answer(
        "Reset was successful!",
        reply_markup=keyboard,
    )

    await state.clear()


@main.message(F.text.lower() == "start")
@main.message(Command("start"))
async def start_handler(message: Message, state: FSMContext) -> None:
    keyboard = keyboard_build(share + reset)

    await message.answer(
        "Please share your number to login in bot",
        reply_markup=keyboard,
    )
    await state.set_state(AllStates.no_login)
