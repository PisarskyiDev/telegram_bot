from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from api.open_ai.ai_config import send_to_ai, check_by_ai
from bot.admin.core import find_command
from bot.buttons import keyboard
from bot.filter.admin_filter import NoAdmin
from bot.states.state import AllStates
from db.engine import session
from db.orm import save_message, get_last_message

ai = Router()


@ai.message(F.text.lower()[0] == "?", NoAdmin())
async def command_handler_by_ai(
    message: types.Message, state: FSMContext
) -> None:
    await message.reply("Your query was accepted, please wait...")
    response = await check_by_ai(text=message.text)
    if response != "404":
        command = find_command(name=response)
        if command is not None:
            await command(message=message, state=state, ai=True)
    else:
        await message.reply("No command found, please try again")


@ai.message(F.text.lower()[0] == "?", AllStates.login)
@ai.message(F.text.lower()[0] == "?", AllStates.no_login)
async def no_admin_rights(message: types.Message) -> None:
    await message.answer("You dont have admin rights for this command")


@ai.message(AllStates.login)
async def gpt_on_handler(message: types.Message) -> None:
    kb = keyboard.default_kb
    previous_massage = await get_last_message(message=message, db=session)
    try:
        await message.reply("Please wait a little bit, i`m thinking...")
        response_ai = await send_to_ai(
            question=message.text,
            previous_answer=previous_massage.answer
            if previous_massage
            else None,
            previous_question=previous_massage.question
            if previous_massage
            else None,
        )

        await message.answer(
            text=response_ai,
            reply_markup=kb,
        )
        await save_message(message=message, answer=response_ai, db=session)
    except TypeError as e:
        await message.answer("Nice try!")
