from tkinter.tix import Form

from aiogram import types, Router, F, html
from aiogram.filters import CommandStart, Command, StateFilter, Filter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    Message,
    ReplyKeyboardRemove,
)


# All handlers should be attached to the Router (or Dispatcher)
router = Router()


class Form(StatesGroup):
    here = State()
    start = State()
    registration = State()
    enter_email = State()
    confirm_email = State()
    pass_email = State()
    before_finish = State()


buttons_start = [
    [
        types.KeyboardButton(text="Here"),
        types.KeyboardButton(text="Website"),
        types.KeyboardButton(request_contact=True, text="Share profile"),
    ]
]

buttons_yes_no = [
    [
        types.KeyboardButton(text="Correct"),
        types.KeyboardButton(text="Edit"),
    ]
]


def get_clear_data(message: Message) -> dict:
    data = {
        "URL": "",
        "email": "",
        "password": "",
    }
    entities = message.entities
    for item in entities:
        for item.type in data.keys():
            data[item.type] = item.extract_from(message.text)

    return data


@router.message(Command("clear"))
async def command_clear_handler(message: Message, state: FSMContext) -> None:
    """
    This handler receives messages with `/clear` command
    """
    await state.clear()
    await message.answer(
        "Cleared!",
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    """
    This handler receives messages with `/start` command
    """
    await state.set_state(Form.registration)
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=buttons_start,
        resize_keyboard=True,
        input_field_placeholder="Which choose?",
    )

    await message.answer(
        "To use this bot you need to register on it first. Were you want to do it?",
        reply_markup=keyboard,
    )
    await state.set_state(Form.registration)


@router.message(F.text.lower() == "here")
@router.message(Form.registration)
async def command_here_handler(message: Message, state: FSMContext) -> None:
    """
    This handler receives messages with `here` text
    """
    await state.set_state(Form.enter_email)
    await message.answer(
        text="Enter your email:",
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(Form.enter_email)
async def email_handler(message: Message, state: FSMContext) -> None:
    """
    This handler receives messages with `email` text
    """
    await state.set_state(Form.confirm_email)
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=buttons_yes_no,
        resize_keyboard=True,
        input_field_placeholder="Which choose?",
    )

    data = get_clear_data(message)
    await message.reply(
        f"Email {html.quote(data['email'])} is correct?", reply_markup=keyboard
    )


@router.message(Form.confirm_email)
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


async def password_handler(message: Message, state: FSMContext) -> None:
    """
    This handler receives messages with `password` text
    """
    await state.set_state(Form.enter_password)
    await message.answer(
        text="Enter your password:",
    )


@router.message(Command)
@router.message()
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
