from aiogram import Router, types, html, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.fsm.storage.base import StorageKey

from bot.buttons.keyboard import (
    reset,
    correct_edit,
    registrate,
    ai_on,
)
from api.service import (
    get_clear_data,
    generate_password,
    send_request_to_api,
)
from bot.states.state import AllStates
from settings.config import LOGIN, PASSWORD, TOKEN_URL, REGISTRATE_URL

checkout = Router()


@checkout.message(AllStates.enter_email)
async def email_handler(message: Message, state: FSMContext) -> None:
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=correct_edit + reset,
        resize_keyboard=True,
        input_field_placeholder="Which choose?",
    )

    data = get_clear_data(message)
    await message.reply(
        f"Email {html.quote(data['email'])} is correct?", reply_markup=keyboard
    )
    await state.storage.set_data(
        key=StorageKey(
            bot_id=message.bot.id,
            user_id=message.from_user.id,
            chat_id=message.chat.id,
        ),
        data={
            "details": {
                "password": generate_password(),
                "email": data["email"],
            },
        },
    )
    await state.set_state(AllStates.confirm_email)


@checkout.message(AllStates.confirm_email)
async def correct_email_handler(message: Message, state: FSMContext) -> None:
    """
    This handler receives messages with `check_email` text
    """
    from_redis = await state.storage.get_data(
        key=StorageKey(
            bot_id=message.bot.id,
            user_id=message.from_user.id,
            chat_id=message.chat.id,
        )
    )
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=registrate + reset,
        resize_keyboard=True,
        input_field_placeholder="Confirm?",
    )
    await message.reply(
        "Here you login: {login} and here you password: {password}".format(
            login=from_redis["details"]["email"],
            password=from_redis["details"]["password"],
        ),
        reply_markup=keyboard,
    )

    token_admin = await send_request_to_api(
        email=LOGIN, password=PASSWORD, url=TOKEN_URL
    )
    await state.set_state(AllStates.ready)

    await state.storage.set_data(
        key=StorageKey(
            bot_id=message.bot.id,
            user_id=message.from_user.id,
            chat_id=message.chat.id,
        ),
        data={
            "details": from_redis["details"],
            "token_admin": {
                "access": token_admin["access"],
                "refresh": token_admin["refresh"],
            },
        },
    )


@checkout.message(AllStates.ready)
async def before_finish_handler(message: Message, state: FSMContext) -> None:
    from_redis = await state.storage.get_data(
        key=StorageKey(
            bot_id=message.bot.id,
            user_id=message.from_user.id,
            chat_id=message.chat.id,
        )
    )

    response = await send_request_to_api(
        email=from_redis["details"]["email"],
        password=from_redis["details"]["password"],
        url=REGISTRATE_URL,
        token=from_redis["token_admin"]["access"],
    )

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=ai_on + reset,
        resize_keyboard=True,
        input_field_placeholder="Ai On?",
    )
    if response["response"] == 201:
        await state.set_state(AllStates.successful)

        await message.reply(
            f"Registration successful! \nYour login: {from_redis['details']['email']}\n"
            f"Your password: {from_redis['details']['password']}",
            reply_markup=keyboard,
        )
    else:
        await state.set_state(AllStates.error)

        await message.reply(
            "Something went wrong! Re-try later",
            reply_markup=types.ReplyKeyboardRemove(),  # TODO add start/reset keyboard
        )


@checkout.message(AllStates.check_login)
async def token_user_handler(message: Message, state: FSMContext) -> None:
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=ai_on + reset,
        resize_keyboard=True,
        input_field_placeholder="Confirm?",
    )

    data = get_clear_data(message, password=True)
    token_user = await send_request_to_api(
        email=data["email"],
        password=data["password"],
        url=TOKEN_URL,
    )

    if token_user["response"] == 200:
        await state.storage.set_data(
            key=StorageKey(
                bot_id=message.bot.id,
                user_id=message.from_user.id,
                chat_id=message.chat.id,
            ),
            data={
                "details": {
                    "email": data["email"],
                    "password": data["password"],
                },
                "token_user": {
                    "access": token_user["access"],
                    "refresh": token_user["refresh"],
                },
            },
        )
        await message.reply(
            f"Login successful!",
            reply_markup=keyboard,
        )
        await state.set_state(AllStates.logged_ai_off)
    else:
        await message.reply(
            "Something went wrong! Re-try later",
            reply_markup=types.ReplyKeyboardRemove(),
        )
        await state.set_state(AllStates.error)


@checkout.message(F.text.lower() == "login", AllStates.no_login)
async def login_handler(message: Message, state: FSMContext) -> None:
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=reset,
        resize_keyboard=True,
        input_field_placeholder="Confirm?",
    )
    await message.reply(
        "Enter your email, and password put like this: (password)",
        reply_markup=keyboard,
    )
    await state.set_state(AllStates.check_login)
