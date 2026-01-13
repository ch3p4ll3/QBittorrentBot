import asyncio
import logging
import sys
from os import getenv

from bot.handlers.on_message import get_router
from redis_helper.wrapper import RedisWrapper

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

# Bot token can be obtained via https://t.me/BotFather
TOKEN = getenv("BOT_TOKEN")


async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN_V2))

    # All handlers should be attached to the Router (or Dispatcher)
    dp = Dispatcher()
    
    # create Redis client
    redis_client = RedisWrapper(url="redis://localhost:6379")
    await redis_client.connect()

    # register it in dp.dependencies
    dp["redis"] = redis_client

    # register routers
    dp.include_router(get_router())

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
