from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from api.nova_ai.config import send_to_ai
from bot.commands.buttons import cancel, gpt_off, gpt_on
from bot.filters.states import Form as States

message_handler = Router()


@message_handler.message(States.confirm_email, F.text.lower() == "edit")
async def edit_email_handler(message: Message, state: FSMContext) -> None:
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=cancel,
    )
    await state.clear()
    await message.answer(
        text="Enter your email:",
        reply_markup=keyboard,
    )
    await state.set_state(States.enter_email)


@message_handler.message(States.no_login, F.text.lower() == "here")
async def here_handler(message: Message, state: FSMContext) -> None:
    """
    This handler receives messages with `here` text
    """
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=cancel,
    )
    await message.answer(
        text="Enter your email:",
        reply_markup=keyboard,
    )

    await state.set_state(States.enter_email)


@message_handler.message(States.login_gpt_on)
async def echo_handler_gpt_on(message: types.Message) -> None:
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=cancel + gpt_off,
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


@message_handler.message(States.login_gpt_off)
async def echo_handler_gpt_off(message: types.Message) -> None:
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=cancel + gpt_on,
    )
    await message.answer(
        text="Gpt is off, and this is simple echo answer",
        reply_markup=keyboard,
    )
