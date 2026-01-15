import asyncio
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from watchfiles import awatch

from bot.handlers import get_commands_router, get_on_message_router
from bot.handlers.callbacks import get_category_router, get_add_torrents_router, get_list_router, \
    get_torrent_info_router, get_resume_router, get_pause_router, get_delete_one_router, \
    get_delete_all_router, get_settings_router

from bot.middlewares import UserMiddleware

from utils import torrent_finished
from redis_helper.wrapper import RedisWrapper
from settings import Settings
from logger import configure_logger



async def watch_config(path: Path, settings: Settings):
    async for _ in awatch(path):
        try:
            new_settings = Settings.load_settings()
            settings.update_from(new_settings)
            print("Settings reloaded successfully")
        except Exception as e:
            print("Failed to reload settings:", e)


async def main(base_path: Path) -> None:
    settings = Settings.load_settings()

    # Initialize Bot instance with default bot properties which will be passed to all API calls
    session = None

    if settings.telegram.proxy is not None:
        session = AiohttpSession(proxy=settings.telegram.proxy.connection_string)

    bot = Bot(token=settings.telegram.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN), session=session)

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
    dp.include_router(get_list_router())
    dp.include_router(get_torrent_info_router())

    dp.include_router(get_category_router())
    dp.include_router(get_resume_router())
    dp.include_router(get_pause_router())
    dp.include_router(get_delete_one_router())
    dp.include_router(get_delete_all_router())
    dp.include_router(get_settings_router())

    # create torrent_finished job
    scheduler = AsyncIOScheduler()
    scheduler.add_job(torrent_finished, "interval", args=[bot, redis_client, settings], seconds=60)
    scheduler.start()

    # create background task for file watching
    watcher_task = asyncio.create_task(
        watch_config(base_path / "data/config.yml", settings)
    )

    # start bot polling (this runs forever)
    try:
        await dp.start_polling(bot)
    finally:
        watcher_task.cancel()


if __name__ == "__main__":
    base_path = Path(__file__).parent.parent

    configure_logger(base_path)
    asyncio.run(main(base_path))
