from aiogram import Bot
from logging import getLogger
from pathlib import Path
from watchfiles import awatch

from src.redis_helper.wrapper import RedisWrapper
from src.client_manager.client_repo import ClientRepo
from src.settings import Settings
from src.settings.user import User


logger = getLogger(__name__)


def user_filters(users: list[User], category: str):
    for user in users:
        if not user.notification_filter:
            yield user

        elif category in user.notification_filter:
            yield user


async def torrent_finished(bot: Bot, redis: RedisWrapper, settings: Settings):
    repository_class = ClientRepo.get_client_manager(settings.client.type)

    for i in await repository_class(settings).get_torrents(status_filter="completed"):
        if not await redis.exists(i.hash):

            for user in user_filters(settings.users, i.category):
                if user.notify:
                    try:
                        await bot.send_message(user.user_id, f"torrent {i.name} has finished downloading!")
                    except:
                        pass

            await redis.set(i.hash, True, 10 * 86400)  # store for 10 days


async def watch_config(path: Path, settings: Settings):
    async for _ in awatch(path):
        try:
            new_settings = Settings.load_settings()
            settings.update_from(new_settings)
            logger.debug("Settings reloaded successfully")
        except Exception as e:
            logger.exception(e)
