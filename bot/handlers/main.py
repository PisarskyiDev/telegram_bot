from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.admin.command import Commands
from bot.buttons import keyboard
from bot.filter.admin_rights import AdminRights
from bot.filter.contact import FilterContact
from bot.states.state import AllStates
from db.engine import session
from db.orm import register_user, select_user

main = Router()


@main.message(F.text.lower() == "cancel")
async def cancel(message: Message, state: FSMContext) -> None:
    await message.answer("Cancelled", reply_markup=keyboard.default_kb)
    await state.set_state(AllStates.login)


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


@main.message(F.text.lower() == "add admin", AdminRights())
async def give_admin(message: Message, state: FSMContext) -> None:
    await message.reply("Send username to GIVE him admin rights")
    await state.set_state(AllStates.waiting_for_give)


@main.message(F.text.lower() == "del admin", AdminRights())
async def take_admin(message: Message, state: FSMContext) -> None:
    await message.reply("Send username to TAKE him admin rights")
    await state.set_state(AllStates.waiting_for_take)


@main.message(F.text.lower() == "all users", AdminRights())
async def call_all_users(message: Message, state: FSMContext) -> None:
    await Commands.all_users(message, state, ai=False)


@main.message(F.text.lower() == "battery power", AdminRights())
async def call_battery_power(message: Message) -> None:
    await Commands.battery_power(message, session, ai=False)


@main.message(AllStates.waiting_for_give)
async def waiting_for_give(
    message: Message, state: FSMContext, _ai: bool = False
) -> None:
    await message.reply("Please wait...")
    response = await Commands.add_admin(message, state)
    if response is None:
        await message.reply("Something went wrong, maybe user not found")
    await state.set_state(AllStates.admin_mode)


@main.message(AllStates.waiting_for_take)
async def waiting_for_take(
    message: Message, state: FSMContext, _ai: bool = False
) -> None:
    await message.reply("Please wait...")
    response = await Commands.del_admin(message, state)
    if response is None:
        await message.reply("Something went wrong, maybe user not found")
