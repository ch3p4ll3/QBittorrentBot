from pyrogram import Client
from pyrogram.types import CallbackQuery
from .... import custom_filters
from .... import db_management
from ..common import list_active_torrents, send_menu


@Client.on_callback_query(filters=custom_filters.list_filter)
async def list_callback(client: Client, callback_query: CallbackQuery) -> None:
    await list_active_torrents(client, 0, callback_query.from_user.id, callback_query.message.id,
                               db_management.read_support(callback_query.from_user.id))


@Client.on_callback_query(filters=custom_filters.list_by_status_filter)
async def list_by_status_callback(client: Client, callback_query: CallbackQuery) -> None:
    status_filter = callback_query.data.split("#")[1]
    await list_active_torrents(client,0, callback_query.from_user.id, callback_query.message.id,
                               db_management.read_support(callback_query.from_user.id), status_filter=status_filter)

@Client.on_callback_query(filters=custom_filters.menu_filter)
async def menu_callback(client: Client, callback_query: CallbackQuery) -> None:
    await send_menu(client, callback_query.message.id, callback_query.from_user.id)
