import asyncio
from pathlib import Path
from os import getenv

from bot.handlers import get_commands_router, get_on_message_router
from bot.handlers.callbacks import get_category_router, get_add_torrents_router
from bot.middlewares import UserMiddleware

from redis_helper.wrapper import RedisWrapper
from settings import Settings
from logger import configure_logger

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode


async def main() -> None:
    settings = Settings.load_settings()

    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=settings.telegram.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))

    # All handlers should be attached to the Router (or Dispatcher)
    dp = Dispatcher()
    
    # create Redis client
    redis_client = RedisWrapper(url=settings.redis.url)
    await redis_client.connect()

    # register it in dp.dependencies
    dp["redis"] = redis_client
    dp["settings"] = settings

    dp.message.middleware(UserMiddleware(settings))
    dp.callback_query.middleware(UserMiddleware(settings))

    # register routers
    dp.include_router(get_on_message_router())
    dp.include_router(get_commands_router())
    dp.include_router(get_add_torrents_router())
    dp.include_router(get_category_router())

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    base_path = Path(__file__).parent.parent

    configure_logger(base_path)
    asyncio.run(main())
