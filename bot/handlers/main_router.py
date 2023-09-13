from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove, Message

from bot.commands.buttons import start, cancel
from bot.filters.states import Form as States

main_handler = Router()


@main_handler.message(Command("cancel"))
async def command_cancel_handler(message: Message, state: FSMContext) -> None:
    """
    This handler receives messages with "cancel" or "exit" or "clear" commands
    """
    await state.clear()
    (
        await message.answer(
            "Canceled!",
            reply_markup=ReplyKeyboardRemove(),
        )
    )


@main_handler.message(F.text.lower() == "cancel")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    """
    This handler receives messages with "cancel" or "exit" or "clear" commands
    """
    await state.clear()
    await message.answer(
        "Canceled!",
        reply_markup=ReplyKeyboardRemove(),
    )


@main_handler.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    """
    This handler receives messages with `/start` command
    """
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=start + cancel,
        resize_keyboard=True,
        input_field_placeholder="Which choose?",
    )

    await message.answer(
        "To use this bot you need to register on it first. Were you want to do it?",
        reply_markup=keyboard,
    )
    await state.set_state(States.registration)
