from aiogram import Router, types, html
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.fsm.storage.base import StorageKey

from bot.commands.buttons import cancel, correct_edit, registrate
from api.services import (
    get_clear_data,
    generate_password,
    send_request_to_api,
)
from bot.filters.states import Form as States
from settings.config import LOGIN, PASSWORD, TOKEN_URL, REGISTRATE_URL

state_handler = Router()


@state_handler.message(States.enter_email)
async def email_handler(message: Message, state: FSMContext) -> None:
    """
    This handler receives messages with `email` text
    """
    await state.clear()
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=correct_edit + cancel,
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
    await state.set_state(States.confirm_email)


@state_handler.message(States.confirm_email)
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
        keyboard=registrate,
        resize_keyboard=True,
        input_field_placeholder="Confirm?",  # TODO refactoring this buttons after separate registrate section–––––––––
    )
    await message.reply(
        "Here you login: {login} and here you password: {password}".format(
            login=from_redis["details"]["email"],
            password=from_redis["details"]["password"],
        ),
        reply_markup=keyboard,
    )

    token = await send_request_to_api(
        email=LOGIN, password=PASSWORD, url=TOKEN_URL
    )

    await state.set_state(States.before_finish)

    response = await send_request_to_api(
        email=from_redis["details"]["email"],
        password=from_redis["details"]["password"],
        url=REGISTRATE_URL,
        token=token["access"],
    )  # TODO separate logic –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

    print(response)
    await state.set_state(States.successful)
