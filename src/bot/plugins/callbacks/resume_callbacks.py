from pyrogram import Client
from pyrogram.types import CallbackQuery

from ... import custom_filters
from ....qbittorrent_manager import QbittorrentManagement
from ..common import list_active_torrents, send_menu


@Client.on_callback_query(filters=custom_filters.resume_all_filter)
async def resume_all_callback(client: Client, callback_query: CallbackQuery) -> None:
    with QbittorrentManagement() as qb:
        qb.resume_all()
    await client.answer_callback_query(callback_query.id, "Resumed all torrents")


@Client.on_callback_query(filters=custom_filters.resume_filter)
async def resume_callback(client: Client, callback_query: CallbackQuery) -> None:
    if callback_query.data.find("#") == -1:
        await list_active_torrents(client, 1, callback_query.from_user.id, callback_query.message.id, "resume")

    else:
        with QbittorrentManagement() as qb:
            qb.resume(torrent_hash=callback_query.data.split("#")[1])
        await send_menu(client, callback_query.message.id, callback_query.from_user.id)
