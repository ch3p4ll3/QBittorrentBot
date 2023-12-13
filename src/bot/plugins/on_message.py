import os
import tempfile

from pyrogram import Client, filters
from pyrogram.types import Message
from ...qbittorrent_manager import QbittorrentManagement
from ... import db_management
from .common import send_menu


@Client.on_message(filters=~filters.me)
async def on_text(client: Client, message: Message) -> None:
    action = db_management.read_support(message.from_user.id)

    if "magnet" in action:
        if message.text.startswith("magnet:?xt"):
            magnet_link = message.text.split("\n")
            category = db_management.read_support(message.from_user.id).split("#")[1]

            with QbittorrentManagement() as qb:
                qb.add_magnet(magnet_link=magnet_link,
                              category=category)

            await send_menu(client, message.id, message.from_user.id)
            db_management.write_support("None", message.from_user.id)

        else:
            await client.send_message(message.from_user.id, "This magnet link is invalid! Retry")

    elif "torrent" in action and message.document:
        if ".torrent" in message.document.file_name:
            with tempfile.TemporaryDirectory() as tempdir:
                name = f"{tempdir}/{message.document.file_name}"
                category = db_management.read_support(message.from_user.id).split("#")[1]
                await message.download(name)

                with QbittorrentManagement() as qb:
                    qb.add_torrent(file_name=name,
                                   category=category)
            await send_menu(client, message.id, message.from_user.id)
            db_management.write_support("None", message.from_user.id)

        else:
            await client.send_message(message.from_user.id, "This is not a torrent file! Retry")

    elif action == "category_name":
        db_management.write_support(f"category_dir#{message.text}", message.from_user.id)
        await client.send_message(message.from_user.id, f"now send me the path for the category {message.text}")

    elif "category_dir" in action:
        if os.path.exists(message.text):
            name = db_management.read_support(message.from_user.id).split("#")[1]

            if "modify" in action:
                with QbittorrentManagement() as qb:
                    qb.edit_category(name=name,
                                     save_path=message.text)
                await send_menu(client, message.id, message.from_user.id)
                return

            with QbittorrentManagement() as qb:
                qb.create_category(name=name,
                                   save_path=message.text)
            await send_menu(client, message.id, message.from_user.id)

        else:
            await client.send_message(message.from_user.id, "The path entered does not exist! Retry")

    else:
        await client.send_message(message.from_user.id, "The command does not exist")
