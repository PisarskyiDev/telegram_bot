from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove, Message
from bot.filters.states import Form as States

message_handler = Router()


@message_handler.message(States.confirm_email and F.text.lower() == "edit")
async def command_edit_email_handler(
    message: Message, state: FSMContext
) -> None:
    await state.clear()
    await message.answer(
        text="Enter your email:",
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.set_state(States.enter_email)


@message_handler.message(F.text.lower() == "here")
async def command_here_handler(message: Message, state: FSMContext) -> None:
    """
    This handler receives messages with `here` text
    """
    await message.answer(
        text="Enter your email:",
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.set_state(States.enter_email)


@message_handler.message(Command)
@message_handler.message()
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
