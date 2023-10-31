import asyncio
import logging
import multiprocessing
import sys

from aiogram.fsm.strategy import FSMStrategy
from aiohttp import web

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from aiogram.webhook.aiohttp_server import (
    SimpleRequestHandler,
    setup_application,
)
from redis.asyncio import Redis

from bot.admin.aschedule import start_schedule
from bot.handlers.main import main
from bot.handlers.text import ai
from bot.handlers.no_handler import no_handler

from settings.config import (
    TOKEN,
    LOCAL,
    PORT,
    WEBHOOK_SECRET,
    WEBHOOK_PATH,
    REDIS_PASSWORD,
    REDIS_HOST,
    REDIS_PORT,
    REDIS_USER,
    HOST,
)
from settings.redis import RedisStorage


async def on_startup(bot: Bot) -> None:
    await bot.set_webhook(f"{HOST}{WEBHOOK_PATH}", secret_token=WEBHOOK_SECRET)


def run() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(
        storage=RedisStorage(
            redis=Redis(
                host=REDIS_HOST,
                port=REDIS_PORT,
                username=REDIS_USER,
                password=REDIS_PASSWORD,
            )
        ),
        fsm_strategy=FSMStrategy.CHAT,
    )

    dp.include_routers(
        main,
        ai,
        no_handler,
    )

    dp.startup.register(on_startup)

    app = web.Application()

    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=WEBHOOK_SECRET,
    )
    webhook_requests_handler.register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)
    web.run_app(app, host=LOCAL, port=PORT)


def start_multi_schedule():
    loop = asyncio.new_event_loop()
    loop.create_task(start_schedule())
    loop.run_forever()


if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR, stream=sys.stdout)
    schedule_process = multiprocessing.Process(target=start_multi_schedule)
    schedule_process.start()
    run()
