from pyrogram import Client
from pyrogram.types import CallbackQuery

from .... import custom_filters
from ....qbittorrent_manager import QbittorrentManagement
from ..common import list_active_torrents, send_menu


@Client.on_callback_query(filters=custom_filters.pause_all_filter)
async def pause_all_callback(client: Client, callback_query: CallbackQuery) -> None:
    with QbittorrentManagement() as qb:
        qb.pause_all()
    await client.answer_callback_query(callback_query.id, "Paused all torrents")


@Client.on_callback_query(filters=custom_filters.pause_filter)
async def pause_callback(client: Client, callback_query: CallbackQuery) -> None:
    if callback_query.data.find("#") == -1:
        await list_active_torrents(client, 1, callback_query.from_user.id, callback_query.message.id, "pause")

    else:
        with QbittorrentManagement() as qb:
            qb.pause(torrent_hash=callback_query.data.split("#")[1])
        await send_menu(client, callback_query.message.id, callback_query.from_user.id)
