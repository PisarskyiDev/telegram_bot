import logging
import sys

from aiohttp import web

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from aiogram.webhook.aiohttp_server import (
    SimpleRequestHandler,
    setup_application,
)
from redis.asyncio import Redis

from bot.handlers.main_router import main_handler
from bot.handlers.message_router import message_handler
from bot.handlers.no_router import no_handler
from bot.handlers.state_router import state_handler

from settings.config import (
    TOKEN,
    LOCAL,
    PORT,
    TEST_HOST,
    WEBHOOK_SECRET,
    WEBHOOK_PATH,
    REDIS_PASSWORD,
    REDIS_HOST,
    REDIS_PORT,
    REDIS_USER, TELEGRAM_HOST,
)

from settings.redis import RedisStorage


WEB_SERVER_HOST = LOCAL
WEB_SERVER_PORT = PORT


async def on_startup(bot: Bot) -> None:
    await bot.set_webhook(
        f"{TELEGRAM_HOST}{WEBHOOK_PATH}", secret_token=WEBHOOK_SECRET
    )


def main() -> None:
    dp = Dispatcher(
        storage=RedisStorage(
            redis=Redis(
                host=REDIS_HOST,
                port=REDIS_PORT,
                username=REDIS_USER,
                password=REDIS_PASSWORD,
            )
        )
    )

    dp.include_routers(
        main_handler,
        state_handler,
        message_handler,
        no_handler,
    )

    dp.startup.register(on_startup)

    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)

    app = web.Application()

    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=WEBHOOK_SECRET,
    )
    webhook_requests_handler.register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)
    web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)


if __name__ == "__main__":
    # logging.basicConfig(level=logging.INFO, filename="bot.log")
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    main()
