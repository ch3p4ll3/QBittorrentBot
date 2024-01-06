import logging
import os
import tempfile
from pyrogram import Client, filters
from pyrogram.types import Message
from ...client_manager import ClientRepo
from ... import db_management
from .common import send_menu
from ...configs import Configs
from ...configs.user import User
from ...utils import convert_type_from_string, inject_user
from .. import custom_filters
from ...translator import Translator, Strings


logger = logging.getLogger(__name__)


async def on_magnet(client, message, user):
    if message.text.startswith("magnet:?xt"):
        magnet_link = message.text.split("\n")
        category = db_management.read_support(message.from_user.id).split("#")[1]

        repository = ClientRepo.get_client_manager(Configs.config.client.type)
        response = repository.add_magnet(
            magnet_link=magnet_link,
            category=category
        )

        if not response:
            await message.reply_text(Translator.translate(Strings.UnableToAddMagnet, locale=user.locale))
            return

        await send_menu(client, message.id, message.from_user.id)
        db_management.write_support("None", message.from_user.id)

    else:
        await client.send_message(
            message.from_user.id,
            Translator.translate(Strings.InvalidMagnet, locale=user.locale)
        )


async def on_torrent(client, message, user):
    if ".torrent" in message.document.file_name:
        with tempfile.TemporaryDirectory() as tempdir:
            name = f"{tempdir}/{message.document.file_name}"
            category = db_management.read_support(message.from_user.id).split("#")[1]
            await message.download(name)

            repository = ClientRepo.get_client_manager(Configs.config.client.type)
            response = repository.add_torrent(file_name=name, category=category)

            if not response:
                await message.reply_text(Translator.translate(Strings.UnableToAddTorrent, locale=user.locale))
                return

        await send_menu(client, message.id, message.from_user.id)
        db_management.write_support("None", message.from_user.id)

    else:
        await client.send_message(
            message.from_user.id,
            Translator.translate(Strings.InvalidTorrent, locale=user.locale)
        )


async def on_category_name(client, message):
    db_management.write_support(f"category_dir#{message.text}", message.from_user.id)
    await client.send_message(
        message.from_user.id,
        Translator.translate(Strings.CategoryPath, category_name=message.text)
    )


async def on_category_directory(client, message, action):
    name = db_management.read_support(message.from_user.id).split("#")[1]

    repository = ClientRepo.get_client_manager(Configs.config.client.type)

    if "modify" in action:
        repository.edit_category(name=name, save_path=message.text)

        await send_menu(client, message.id, message.from_user.id)
        return

    repository.create_category(name=name, save_path=message.text)

    await send_menu(client, message.id, message.from_user.id)


async def on_edit_user(client, message, user, action):
    data = action.split("#")[1]
    user_id = int(data.split("-")[0])
    field_to_edit = data.split("-")[1]
    data_type = convert_type_from_string(data.split("-")[2].replace("<class ", "").replace(">", ""))

    try:
        new_value = data_type(message.text)

        user_from_configs = Configs.config.users.index(user)

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

        setattr(Configs.config.users[user_from_configs], field_to_edit, new_value)
        Configs.update_config(Configs.config)
        Configs.reload_config()
        logger.debug(f"Updating User #{user_id} {field_to_edit} settings to {new_value}")
        db_management.write_support("None", message.from_user.id)

        await send_menu(client, message.id, message.from_user.id)
    except Exception as e:
        await message.reply_text(Translator.translate(Strings.GenericError, locale=user.locale, error=e))
        logger.exception(f"Error converting value \"{message.text}\" to type \"{data_type}\"", exc_info=True)


async def on_edit_client(client: Client, message: Message, user, action):
    data = action.split("#")[1]
    field_to_edit = data.split("-")[0]
    data_type = convert_type_from_string(data.split("-")[1])

    try:
        new_value = data_type(message.text)

        setattr(Configs.config.client, field_to_edit, new_value)
        Configs.update_config(Configs.config)
        Configs.reload_config()
        logger.debug(f"Updating Client field \"{field_to_edit}\" to \"{new_value}\"")
        db_management.write_support("None", message.from_user.id)

        await send_menu(client, message.id, message.from_user.id)
    except Exception as e:
        await message.reply_text(Translator.translate(Strings.GenericError, locale=user.locale, error=e))
        logger.exception(f"Error converting value \"{message.text}\" to type \"{data_type}\"", exc_info=True)


@Client.on_message(~filters.me & custom_filters.check_user_filter)
@inject_user
async def on_text(client: Client, message: Message, user: User) -> None:
    action = db_management.read_support(message.from_user.id)

    if "magnet" in action:
        await on_magnet(client, message, user)

    elif "torrent" in action and message.document:
        await on_torrent(client, message, user)

    elif action == "category_name":
        await on_category_name(client, message)

    elif "category_dir" in action:
        await on_category_directory(client, message, action)

    elif "edit_user" in action:
        await on_edit_user(client, message, user, action)

    elif "edit_clt" in action:
        await on_edit_client(client, message, user, action)

    else:
        await client.send_message(
            message.from_user.id,
            Translator.translate(Strings.CommandDoesNotExist, locale=user.locale)
        )
