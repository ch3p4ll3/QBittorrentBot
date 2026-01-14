from pyrogram import Client
from pyrogram.types import CallbackQuery
from .... import db_management
from ...filters import custom_filters
from ....settings.user import User
from ....translator import Translator, Strings
from ....utils import inject_user


@Client.on_callback_query(custom_filters.add_magnet_filter & custom_filters.check_user_filter & (custom_filters.user_is_administrator | custom_filters.user_is_manager))
@inject_user
async def add_magnet_callback(client: Client, callback_query: CallbackQuery, user: User) -> None:
    db_management.write_support(f"magnet#{callback_query.data.split('#')[1]}", callback_query.from_user.id)
    await client.answer_callback_query(callback_query.id, Translator.translate(Strings.SendMagnetLink, user.locale))


@Client.on_callback_query(custom_filters.add_torrent_filter & custom_filters.check_user_filter & (custom_filters.user_is_administrator | custom_filters.user_is_manager))
@inject_user
async def add_torrent_callback(client: Client, callback_query: CallbackQuery, user: User) -> None:
    db_management.write_support(f"torrent#{callback_query.data.split('#')[1]}", callback_query.from_user.id)
    await client.answer_callback_query(callback_query.id, Translator.translate(Strings.SendTorrentFile, user.locale))
