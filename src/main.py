import asyncio
import logging
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeChat
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.utils.i18n import I18n

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from src.bot.handlers import get_commands_router, get_on_message_router, get_rss_router
from src.bot.handlers.callbacks import get_category_router, get_add_torrents_router, get_list_router, \
    get_torrent_info_router, get_resume_router, get_pause_router, get_delete_one_router, \
    get_delete_all_router, get_settings_router, get_rss_buttons_router

from src.bot.middlewares import UserMiddleware, CustomI18nMiddleware

from src.tasks import torrent_finished, watch_config
from src.redis_helper.wrapper import RedisWrapper
from src.settings import Settings
from src.settings.enums import UserRolesEnum
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

    # create Redis client
    redis_client = RedisWrapper(url=settings.redis.url)
    await redis_client.connect()

    # register it in dp.dependencies
    dp["redis"] = redis_client
    dp["settings"] = settings

    dp.message.middleware(UserMiddleware(settings))
    dp.callback_query.middleware(UserMiddleware(settings))
    dp.message.middleware(CustomI18nMiddleware(i18n))
    dp.callback_query.middleware(CustomI18nMiddleware(i18n))

    # register routers
    dp.include_router(get_rss_router())
    dp.include_router(get_rss_buttons_router())
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
    scheduler.add_job(torrent_finished, "interval", args=[bot, redis_client, settings, CustomI18nMiddleware(i18n)], seconds=60)
    scheduler.start()

    # create background task for file watching
    watcher_task = asyncio.create_task(
        watch_config(base_path / "data/config.yml", settings)
    )

    # Show the administrator-only RSS commands in the "/" menu, but only in the chats of administrators: the default
    # command list (for example the one set in BotFather) is left alone and other users never see these commands
    admin_commands = [
        BotCommand(command="start", description="Open the main menu"),
        BotCommand(command="stats", description="System stats"),
        BotCommand(command="rss", description="RSS menu: watch for a name, feeds, rules"),
        BotCommand(command="rss_list", description="Show RSS feeds and rules as text"),
        BotCommand(command="rss_help", description="RSS commands help"),
        BotCommand(command="rss_addfeed", description="Add a feed: name url"),
        BotCommand(command="rss_delfeed", description="Remove a feed: name"),
        BotCommand(command="rss_addrule", description="Add a rule: name ; feed ; contain ; not ; category ; show"),
        BotCommand(command="rss_delrule", description="Remove a rule: name"),
        BotCommand(command="rss_toggle", description="Enable or disable a rule: name"),
    ]
    for user in settings.users:
        if user.role != UserRolesEnum.Administrator:
            continue
        try:
            await bot.set_my_commands(admin_commands, scope=BotCommandScopeChat(chat_id=user.user_id))
        except Exception as e:
            logging.warning(f"Could not set the bot commands for user {user.user_id}: {e}")

    # start bot polling (this runs forever)
    try:
        await dp.start_polling(bot)
    finally:
        watcher_task.cancel()


if __name__ == "__main__":
    base_path = Path(__file__).parent.parent

    configure_logger(base_path)
    asyncio.run(main(base_path))
