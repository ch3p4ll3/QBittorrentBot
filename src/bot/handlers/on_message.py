import logging
import tempfile
from client_manager import ClientRepo
from .common import send_menu
from settings import Settings
from settings.user import User
from utils import convert_type_from_string, inject_user
from ..custom_filters import IsAuthorizedUser
from translator import Translator, Strings
from redis_helper.wrapper import RedisWrapper

from aiogram import F
from aiogram import Bot
from aiogram.types import Message
from aiogram.dispatcher.router import Router


logger = logging.getLogger(__name__)


def get_router():
    router = Router()

    async def on_magnet(message: Message, user, redis: RedisWrapper, bot: Bot, settings: Settings):
        if message.text.startswith("magnet:?xt"):
            magnet_link = message.text.split("\n")
            category = (await redis.get(f"action:{message.from_user.id}")).split("#")[1]

            repository = ClientRepo.get_client_manager(settings.client.type)
            response = repository.add_magnet(
                magnet_link=magnet_link,
                category=category
            )

            if not response:
                await message.reply_text(Translator.translate(Strings.UnableToAddMagnet, locale=user.locale))
                return

            await send_menu(bot, redis, settings, message.chat.id, message.message_id)
            await redis.set(f"action:{message.from_user.id}", None)

        else:
            await message.reply(
                Translator.translate(Strings.InvalidMagnet, locale=user.locale)
            )


    async def on_torrent(message: Message, user, redis: RedisWrapper, bot: Bot, settings: Settings):
        if ".torrent" in message.document.file_name:
            with tempfile.TemporaryDirectory() as tempdir:
                name = f"{tempdir}/{message.document.file_name}"
                category = (await redis.get(f"action:{message.from_user.id}")).split("#")[1]
                await message.download(name)

                repository = ClientRepo.get_client_manager(settings.client.type)
                response = repository.add_torrent(file_name=name, category=category)

                if not response:
                    await message.reply(Translator.translate(Strings.UnableToAddTorrent, locale=user.locale))
                    return

            await send_menu(bot, redis, settings, message.chat.id, message.message_id)
            await redis.set(f"action:{message.from_user.id}", None)

        else:
            await message.reply(
                Translator.translate(Strings.InvalidTorrent, locale=user.locale)
            )


    async def on_category_name(message: Message, redis: RedisWrapper):
        await redis.set(f"action:{message.from_user.id}", f"category_dir#{message.text}")
        await message.reply(
            Translator.translate(Strings.CategoryPath, category_name=message.text)
        )


    async def on_category_directory(message: Message, action, redis: RedisWrapper, bot: Bot, settings: Settings):
        name = (await redis.get(f"action:{message.from_user.id}")).split("#")[1]

        repository = ClientRepo.get_client_manager(settings.client.type)

        if "modify" in action:
            repository.edit_category(name=name, save_path=message.text)
            await send_menu(bot, redis, settings, message.chat.id, message.message_id)
            return

        repository.create_category(name=name, save_path=message.text)
        await send_menu(bot, redis, settings, message.chat.id, message.message_id)


    async def on_edit_user(message: Message, user, action, redis: RedisWrapper, bot: Bot, settings: Settings):
        data = action.split("#")[1]
        user_id = int(data.split("-")[0])
        field_to_edit = data.split("-")[1]
        data_type = convert_type_from_string(data.split("-")[2].replace("<class ", "").replace(">", ""))

        try:
            new_value = data_type(message.text)

            user_from_configs = settings.users.index(user)

            if user_from_configs == -1:
                return

            if field_to_edit == "locale" and new_value not in Translator.locales.keys():
                await message.reply_text(
                    Translator.translate(
                        Strings.LocaleNotFound,
                        locale=user.locale,
                        new_locale=new_value
                    )
                )
                return

            setattr(settings.users[user_from_configs], field_to_edit, new_value)
            # Configs.update_config(settings)
            # Configs.reload_config()
            logger.debug(f"Updating User #{user_id} {field_to_edit} settings to {new_value}")
            await redis.set(f"action:{message.from_user.id}", None)

            await send_menu(bot, redis, settings, message.chat.id, message.message_id)
        except Exception as e:
            await message.reply_text(Translator.translate(Strings.GenericError, locale=user.locale, error=e))
            logger.exception(f"Error converting value \"{message.text}\" to type \"{data_type}\"", exc_info=True)


    async def on_edit_client(message: Message, user, action, redis: RedisWrapper, bot: Bot, settings: Settings):
        data = action.split("#")[1]
        field_to_edit = data.split("-")[0]
        data_type = convert_type_from_string(data.split("-")[1])

        try:
            new_value = data_type(message.text)

            setattr(settings.client, field_to_edit, new_value)
            # Configs.update_config(Settings)
            # Configs.reload_config()
            logger.debug(f"Updating Client field \"{field_to_edit}\" to \"{new_value}\"")
            await redis.set(f"action:{message.from_user.id}", None)

            await send_menu(bot, redis, settings, message.chat.id, message.message_id)
        except Exception as e:
            await message.reply_text(Translator.translate(Strings.GenericError, locale=user.locale, error=e))
            logger.exception(f"Error converting value \"{message.text}\" to type \"{data_type}\"", exc_info=True)


    @router.message(IsAuthorizedUser(), ~F.from_user.is_bot)
    @inject_user
    async def on_message(message: Message, redis: RedisWrapper, bot: Bot, settings: Settings, user: User) -> None:
        action = await redis.get(f"action:{message.from_user.id}")
        print(user)

        if "magnet" in action:
            await on_magnet(message, user, redis, bot, settings)

        elif "torrent" in action and message.document:
            await on_torrent(message, user, redis, bot, settings)

        elif action == "category_name":
            await on_category_name(message, redis, bot, settings)

        elif "category_dir" in action:
            await on_category_directory(message, action, redis, bot, settings)

        elif "edit_user" in action:
            await on_edit_user(message, user, action, redis, bot, settings)

        elif "edit_clt" in action:
            await on_edit_client(message, user, action, redis, bot, settings)
        else:
            await message.reply(
                Translator.translate(Strings.CommandDoesNotExist, locale=user.locale)
            )

    return router
