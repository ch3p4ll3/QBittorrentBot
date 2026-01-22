import logging
import tempfile

from aiogram import F
from aiogram import Bot
from aiogram.types import Message
from aiogram.dispatcher.router import Router
from aiogram.utils.i18n import gettext as _

from src.client_manager.client_repo import ClientRepo
from src.settings import Settings
from src.settings.user import User
from src.bot.filters import IsAuthorizedUser, IsCommand
from src.redis_helper.wrapper import RedisWrapper

from .common import send_menu


logger = logging.getLogger(__name__)


def get_router():
    router = Router()

    async def on_magnet(message: Message, user, redis: RedisWrapper, bot: Bot, settings: Settings):
        if message.text.startswith("magnet:?xt"):
            magnet_link = message.text.split("\n")
            category = (await redis.get(f"action:{message.from_user.id}")).split("#")[1]

            repository_class = ClientRepo.get_client_manager(settings.client.type)
            response = await repository_class(settings).add_magnet(
                magnet_link=magnet_link,
                category=category
            )

            if not response:
                await message.reply(_("Unable to add magnet link"))
                return

            await send_menu(bot, redis, settings, message.chat.id, message.message_id)
            await redis.set(f"action:{message.from_user.id}", None)

        else:
            await message.reply(
                _("This magnet link is invalid! Retry")
            )


    async def on_torrent(message: Message, user, redis: RedisWrapper, bot: Bot, settings: Settings):
        if ".torrent" in message.document.file_name:
            with tempfile.TemporaryDirectory() as tempdir:
                name = f"{tempdir}/{message.document.file_name}"
                category = (await redis.get(f"action:{message.from_user.id}")).split("#")[1]

                file = await bot.get_file(message.document.file_id)
                file_path = file.file_path
                await bot.download_file(file_path, name)

                repository_class = ClientRepo.get_client_manager(settings.client.type)
                response = await repository_class(settings).add_torrent(file_name=name, category=category)

                if not response:
                    await message.reply(_("Unable to add torrent file"))
                    return

            await send_menu(bot, redis, settings, message.chat.id, message.message_id)
            await redis.set(f"action:{message.from_user.id}", None)

        else:
            await message.reply(
                _("This is not a torrent file! Retry")
            )


    async def on_category_name(message: Message, redis: RedisWrapper):
        await redis.set(f"action:{message.from_user.id}", f"category_dir#{message.text}")
        await message.reply(
            _("Please, send the path for the category {category_name}"
                .format(
                    category_name=message.text
                )
            )
        )


    async def on_category_directory(message: Message, action, redis: RedisWrapper, bot: Bot, settings: Settings):
        name: str = (await redis.get(f"action:{message.from_user.id}")).split("#")[1]

        repository_class = ClientRepo.get_client_manager(settings.client.type)

        if "modify" in action:
            await repository_class(settings).edit_category(name=name, save_path=message.text.replace("\\", ""))
            await send_menu(bot, redis, settings, message.chat.id, message.message_id)
            return

        await repository_class(settings).create_category(name=name, save_path=message.text.replace("\\", ""))
        await send_menu(bot, redis, settings, message.chat.id, message.message_id)


    @router.message(~F.from_user.is_bot, ~IsCommand(), IsAuthorizedUser())
    async def on_message(message: Message, redis: RedisWrapper, bot: Bot, settings: Settings, user: User) -> None:
        action = await redis.get(f"action:{message.from_user.id}") or ""

        if "magnet" in action:
            await on_magnet(message, user, redis, bot, settings)

        elif "torrent" in action and message.document:
            await on_torrent(message, user, redis, bot, settings)

        elif action == "category_name":
            await on_category_name(message, redis)

        elif "category_dir" in action:
            await on_category_directory(message, action, redis, bot, settings)

        else:
            await message.reply(
                _("The command does not exist")
            )

    return router
