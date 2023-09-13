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
    REDIS_USER,
)

from settings.redis import RedisStorage


WEB_SERVER_HOST = LOCAL
WEB_SERVER_PORT = PORT


async def on_startup(bot: Bot) -> None:
    await bot.set_webhook(
        f"{TEST_HOST}{WEBHOOK_PATH}", secret_token=WEBHOOK_SECRET
    )


def main() -> None:
    # Dispatcher is a root router
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
    )

    # Register startup hook to initialize webhook
    dp.startup.register(on_startup)

    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)

    # Create aiohttp.web.Application instance
    app = web.Application()

    # Create an instance of request handler,
    # aiogram has few implementations for different cases of usage
    # In this example we use SimpleRequestHandler which is designed to handle simple cases
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=WEBHOOK_SECRET,
    )
    # Register webhook handler on application
    webhook_requests_handler.register(app, path=WEBHOOK_PATH)

    # Mount dispatcher startup and shutdown hooks to aiohttp application
    setup_application(app, dp, bot=bot)

    # And finally start webserver
    web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)


if __name__ == "__main__":
    # logging.basicConfig(level=logging.INFO, filename="bot.log") TODO set logging in file bot.log in prod–––––––––––––
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    main()
