from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.admin.command import Commands
from bot.buttons import keyboard
from bot.filter.contact import FilterContact
from bot.states.state import AllStates
from db.engine import session
from db.orm import register_user, select_user

main = Router()


@main.message(F.text.lower() == "reset")
@main.message(Command("reset"))
async def reset_handler(message: Message, state: FSMContext) -> None:
    kb = keyboard.start_kb

    await message.answer(
        "Reset was successful!",
        reply_markup=kb,
    )

    await state.clear()


@main.message(F.text.lower() == "start")
@main.message(Command("start"))
async def start_handler(message: Message, state: FSMContext) -> None:
    kb = keyboard.build(keyboard.share + keyboard.reset)

    await message.answer(
        "Please share your number to login in bot",
        reply_markup=kb,
    )
    await state.set_state(AllStates.no_login)


@main.message(FilterContact())
async def login_handler(message: Message, state: FSMContext) -> None:
    kb = keyboard.default_kb
    check_state = await state.get_state()
    check_owner = await FilterContact.check_id(message)

    if check_state == AllStates.login:
        text = "You are already logged in!"
    else:
        if not check_owner:
            text = "Number was not confirmed! You can use only your own number"
            await state.set_state(AllStates.no_login)

        else:
            result = await register_user(message=message, db=session)
            if result and isinstance(result, str):
                await state.set_state(AllStates.login)
                text = result
            elif result and isinstance(result, bool):
                text = (
                    "Number confirmed successfully! Your account was created :) "
                    "\nNow you can use this bot"
                )
                await state.set_state(AllStates.login)
            else:
                text = (
                    "Number confirmed successfully! "
                    "But your account was not created! "
                    "\nPlease try again"
                )
    await message.reply(text, reply_markup=kb)


@main.message(F.text.lower() == "profile", AllStates.login)
async def get_profile(message: Message) -> None:
    kb = keyboard.default_kb
    user = await select_user(user_id=message.from_user.id, db=session)
    await message.reply(
        "Your profile:"
        f"\nName: {user.name}"
        f"\nUsername: {user.username}"
        f"\nId: {user.id}"
        f"\nAdmin: {user.admin}",
        reply_markup=kb,
    )


@main.message(F.text.lower() == "admin off", AllStates.admin_mode)
async def admin_off(message: Message, state: FSMContext) -> None:
    await Commands.admin_mode(message, state)


@main.message(F.text.lower() == "admin on", AllStates.login)
async def admin_on(message: Message, state: FSMContext) -> None:
    await Commands.admin_mode(message, state)
