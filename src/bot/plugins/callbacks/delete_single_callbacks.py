from pyrogram import Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from ... import custom_filters
from ....qbittorrent_manager import QbittorrentManagement
from ..common import list_active_torrents, send_menu


@Client.on_callback_query(custom_filters.delete_one_filter)
async def delete_callback(client: Client, callback_query: CallbackQuery) -> None:
    if callback_query.data.find("#") == -1:
        await list_active_torrents(client, 1, callback_query.from_user.id, callback_query.message.id, "delete_one")

    else:

        buttons = [
            [InlineKeyboardButton("🗑 Delete torrent", f"delete_one_no_data#{callback_query.data.split('#')[1]}")],
            [InlineKeyboardButton("🗑 Delete torrent and data", f"delete_one_data#{callback_query.data.split('#')[1]}")],
            [InlineKeyboardButton("🔙 Menu", "menu")]]

        await client.edit_message_reply_markup(callback_query.from_user.id, callback_query.message.id,
                                               reply_markup=InlineKeyboardMarkup(buttons))


@Client.on_callback_query(custom_filters.delete_one_no_data_filter)
async def delete_no_data_callback(client: Client, callback_query: CallbackQuery) -> None:
    if callback_query.data.find("#") == -1:
        await list_active_torrents(client, 1, callback_query.from_user.id, callback_query.message.id, "delete_one_no_data")

    else:
        with QbittorrentManagement() as qb:
            qb.delete_one_no_data(torrent_hash=callback_query.data.split("#")[1])
        await send_menu(client, callback_query.message.id, callback_query.from_user.id)


@Client.on_callback_query(custom_filters.delete_one_data_filter)
async def delete_with_data_callback(client: Client, callback_query: CallbackQuery) -> None:
    if callback_query.data.find("#") == -1:
        await list_active_torrents(client, 1, callback_query.from_user.id, callback_query.message.id, "delete_one_data")

    else:
        with QbittorrentManagement() as qb:
            qb.delete_one_data(torrent_hash=callback_query.data.split("#")[1])
        await send_menu(client, callback_query.message.id, callback_query.from_user.id)
