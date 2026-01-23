import asyncio
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.utils.i18n import I18n
from aiogram.utils.i18n.middleware import SimpleI18nMiddleware

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from src.bot.handlers import get_commands_router, get_on_message_router
from src.bot.handlers.callbacks import get_category_router, get_add_torrents_router, get_list_router, \
    get_torrent_info_router, get_resume_router, get_pause_router, get_delete_one_router, \
    get_delete_all_router, get_settings_router

from src.bot.middlewares import UserMiddleware

from src.tasks import torrent_finished, watch_config
from src.redis_helper.wrapper import RedisWrapper
from src.settings import Settings
from src.logger import configure_logger


async def main(base_path: Path) -> None:
    settings = Settings.load_settings()

    # Initialize Bot instance with default bot properties which will be passed to all API calls
    session = None

    if settings.telegram.proxy is not None:
        session = AiohttpSession(proxy=settings.telegram.proxy.connection_string)

    bot = Bot(
        token=settings.telegram.bot_token,
        default=DefaultBotProperties(
            parse_mode=ParseMode.MARKDOWN
        ),
        session=session
    )

    # All handlers should be attached to the Router (or Dispatcher)
    dp = Dispatcher()


    locales_path = Path(__file__).parent / "locales"
    i18n = I18n(path=locales_path, default_locale="en", domain="messages")
    i18n_middleware = SimpleI18nMiddleware(i18n)
    
    dp.message.middleware(i18n_middleware)
    dp.callback_query.middleware(i18n_middleware)

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
