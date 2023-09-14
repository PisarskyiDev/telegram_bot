from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.commands.buttons import (
    start,
    cancel,
    gpt_off,
    gpt_on,
    registration,
    login,
)
from bot.filters.states import Form as States

main_handler = Router()


@main_handler.message(F.text.lower() == "cancel")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    """
    This handler receives messages with "cancel" or "exit" or "clear" commands
    """
    await state.clear()
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=start + cancel,
        resize_keyboard=True,
        input_field_placeholder="Which choose?",
    )

    await state.clear()
    await message.answer(
        "Canceled!",
        reply_markup=keyboard,
    )


@main_handler.message(F.text.lower() == "gpt on", States.login_gpt_off)
async def gpt_on(message: Message, state: FSMContext) -> None:
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=cancel + gpt_off,
        resize_keyboard=True,
        input_field_placeholder="Gpt off?",
    )
    await message.answer("Gpt is on", reply_markup=keyboard)
    await state.set_state(States.login_gpt_on)


@main_handler.message(F.text.lower() == "gpt off", States.login_gpt_on)
async def gpt_off(message: Message, state: FSMContext) -> None:
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=cancel + gpt_on,
        resize_keyboard=True,
        input_field_placeholder="Gpt on?",
    )
    await message.answer("Gpt is off", reply_markup=keyboard)
    await state.set_state(States.login_gpt_off)


@main_handler.message(F.text.lower() == "start")
async def command_start_handler(message: Message, state: FSMContext) -> None:
    """
    This handler receives messages with `/start` command
    """
    await state.clear()
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=registration + cancel + login,
        # + (gpt_off if await state.get_state() == States.gpt_on else gpt_on),
        resize_keyboard=True,
        input_field_placeholder="Which choose?",
    )

    await message.answer(
        "To use this bot you need to register on it first. Were you want to do it?",
        reply_markup=keyboard,
    )
    await state.set_state(States.no_login)
