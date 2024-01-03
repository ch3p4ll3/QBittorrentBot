import logging
import os
import tempfile
from pyrogram import Client, filters
from pyrogram.types import Message
from ...client_manager import ClientRepo
from ... import db_management
from .common import send_menu
from ...configs import Configs
from ...utils import get_user_from_config, convert_type_from_string
from .. import custom_filters
from ...translator import Translator, Strings


logger = logging.getLogger(__name__)


@Client.on_message(~filters.me & custom_filters.check_user_filter)
async def on_text(client: Client, message: Message) -> None:
    action = db_management.read_support(message.from_user.id)
    user = get_user_from_config(message.from_user.id)

    if "magnet" in action:
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

    elif "torrent" in action and message.document:
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

    elif action == "category_name":
        db_management.write_support(f"category_dir#{message.text}", message.from_user.id)
        await client.send_message(
            message.from_user.id,
            Translator.translate(Strings.CategoryPath, category_name=message.text)
        )

    elif "category_dir" in action:
        if os.path.exists(message.text):
            name = db_management.read_support(message.from_user.id).split("#")[1]

            repository = ClientRepo.get_client_manager(Configs.config.client.type)

            if "modify" in action:
                repository.edit_category(name=name, save_path=message.text)

                await send_menu(client, message.id, message.from_user.id)
                return

            repository.create_category(name=name, save_path=message.text)

            await send_menu(client, message.id, message.from_user.id)

        else:
            await client.send_message(
                message.from_user.id, Translator.translate(Strings.PathNotValid,locale=user.locale)
            )

    elif "edit_user" in action:
        data = action.split("#")[1]
        user_id = int(data.split("-")[0])
        field_to_edit = data.split("-")[1]
        data_type = convert_type_from_string(data.split("-")[2].replace("<class ", "").replace(">", ""))

        try:
            new_value = data_type(message.text)

            user_from_configs = Configs.config.users.index(user)

            if user_from_configs == -1:
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

    elif "edit_clt" in action:
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
    else:
        await client.send_message(
            message.from_user.id,
            Translator.translate(Strings.CommandDoesNotExist, locale=user.locale)
        )
