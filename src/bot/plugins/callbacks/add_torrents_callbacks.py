from pyrogram import Client
from pyrogram.types import CallbackQuery
from .... import db_management
from ... import custom_filters


@Client.on_callback_query(custom_filters.add_magnet_filter)
async def add_magnet_callback(client: Client, callback_query: CallbackQuery) -> None:
    db_management.write_support(f"magnet#{callback_query.data.split('#')[1]}", callback_query.from_user.id)
    await client.answer_callback_query(callback_query.id, "Send a magnet link")


@Client.on_callback_query(custom_filters.add_torrent_filter)
async def add_torrent_callback(client: Client, callback_query: CallbackQuery) -> None:
    db_management.write_support(f"torrent#{callback_query.data.split('#')[1]}", callback_query.from_user.id)
    await client.answer_callback_query(callback_query.id, "Send a torrent file")
