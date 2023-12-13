from pyrogram import Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from .... import custom_filters
from ....qbittorrent_manager import QbittorrentManagement
from ..common import send_menu


@Client.on_callback_query(filters=custom_filters.delete_all_filter)
async def delete_all_callback(client: Client, callback_query: CallbackQuery) -> None:
    buttons = [[InlineKeyboardButton("🗑 Delete all torrents", "delete_all_no_data")],
               [InlineKeyboardButton("🗑 Delete all torrents and data", "delete_all_data")],
               [InlineKeyboardButton("🔙 Menu", "menu")]]
    await client.edit_message_reply_markup(callback_query.from_user.id, callback_query.message.id,
                                           reply_markup=InlineKeyboardMarkup(buttons))


@Client.on_callback_query(filters=custom_filters.delete_all_no_data_filter)
async def delete_all_with_no_data_callback(client: Client, callback_query: CallbackQuery) -> None:
    with QbittorrentManagement() as qb:
        qb.delete_all_no_data()
    await client.answer_callback_query(callback_query.id, "Deleted only torrents")
    await send_menu(client, callback_query.message.id, callback_query.from_user.id)


@Client.on_callback_query(filters=custom_filters.delete_all_data_filter)
async def delete_all_with_data_callback(client: Client, callback_query: CallbackQuery) -> None:
    with QbittorrentManagement() as qb:
        qb.delete_all_data()
    await client.answer_callback_query(callback_query.id, "Deleted All+Torrents")
    await send_menu(client, callback_query.message.id, callback_query.from_user.id)
