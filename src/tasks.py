from aiogram import Bot
from aiogram.utils.i18n import gettext as _

from logging import getLogger
from pathlib import Path
from watchfiles import awatch

from src.utils import escape_markdown
from src.redis_helper.wrapper import RedisWrapper
from src.client_manager.client_repo import ClientRepo
from src.settings import Settings
from src.settings.user import User
from src.bot.middlewares.custom_i18n import CustomI18nMiddleware


logger = getLogger(__name__)


def user_filters(users: list[User], category: str):
    for user in users:
        if not user.notification_filter:
            yield user

        elif category in user.notification_filter:
            yield user


async def torrent_finished(bot: Bot, redis: RedisWrapper, settings: Settings, i18n_middleware: CustomI18nMiddleware):
    repository_class = ClientRepo.get_client_manager(settings.client.type)

    for i in await repository_class(settings).get_torrents(status_filter="completed"):
        if not await redis.exists(i.hash):

            for user in user_filters(settings.users, i.category):
                if user.notify:
                    try:
                        with i18n_middleware.i18n.context() as ctx:
                            user_lang = user.locale if user.locale else ctx.default_locale

                            ctx.use_locale(user_lang)
                            await bot.send_message(
                                user.user_id,
                                _("Torrent {name} has finished downloading!"
                                    .format(
                                        name=escape_markdown(i.name)
                                    )
                                )
                            )
                    except Exception as e:
                        logger.exception(e)

            await redis.set(i.hash, 1, 10 * 86400)  # store for 10 days


async def watch_config(path: Path, settings: Settings):
    async for _ in awatch(path):
        try:
            new_settings = Settings.load_settings()
            settings.update_from(new_settings)
            logger.debug("Settings reloaded successfully")
        except Exception as e:
            logger.exception(e)
