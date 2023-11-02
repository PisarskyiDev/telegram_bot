from aiogram import Router
from aiogram.types import Message

from bot.buttons import keyboard
from bot.filter.banned_filter import Banned

banned = Router()


@banned.message(Banned())
async def banned_handler(message: Message) -> None:
    await message.reply(
        "You are banned from this bot", reply_markup=keyboard.banned_kb
    )
