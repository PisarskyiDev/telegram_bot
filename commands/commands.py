from aiogram import F, html, Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    ReplyKeyboardRemove,
)

from filters.states import Form as Filter
from .buttons import *
from .helpers import *

email = Router()
start = Router()


@start.message(Command("clear"))
async def command_clear_handler(message: Message, state: FSMContext) -> None:
    """
    This handler receives messages with `/clear` command
    """
    await state.clear()
    await message.answer(
        "Cleared!",
        reply_markup=ReplyKeyboardRemove(),
    )


@start.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    """
    This handler receives messages with `/start` command
    """
    await state.set_state(Filter.registration)
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=buttons_start,
        resize_keyboard=True,
        input_field_placeholder="Which choose?",
    )

    await message.answer(
        "To use this bot you need to register on it first. Were you want to do it?",
        reply_markup=keyboard,
    )
    await state.set_state(Filter.registration)


@email.message(F.text.lower() == "here")
@email.message(Filter.registration)
async def command_here_handler(message: Message, state: FSMContext) -> None:
    """
    This handler receives messages with `here` text
    """
    await state.set_state(Filter.enter_email)
    await message.answer(
        text="Enter your email:",
        reply_markup=ReplyKeyboardRemove(),
    )


@email.message(Filter.enter_email)
async def email_handler(message: Message, state: FSMContext) -> None:
    """
    This handler receives messages with `email` text
    """
    await state.set_state(Filter.confirm_email)
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=buttons_yes_no,
        resize_keyboard=True,
        input_field_placeholder="Which choose?",
    )

    data = get_clear_data(message)
    await message.reply(
        f"Email {html.quote(data['email'])} is correct?", reply_markup=keyboard
    )


@email.message(Filter.confirm_email)
async def correct_email_handler(message: Message, state: FSMContext) -> None:
    """
    This handler receives messages with `check_email` text
    """
    await message.reply(
        "Here you login {login} and here you password {passwod}".format(
            login=["email"], passwod=["password"]
        ),
        reply_markup=ReplyKeyboardRemove(),
    )


@email.message(Command)
@email.message()
async def echo_handler(message: types.Message) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like text, photo, sticker etc.)
    """
    try:
        # Send a copy of the received message
        await message.answer(
            "This is echo",
            copy_forwards=True,
            reply_markup=ReplyKeyboardRemove(),
        )
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")
