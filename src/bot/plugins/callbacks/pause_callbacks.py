from pyrogram import Client
from pyrogram.types import CallbackQuery

from ... import custom_filters
from ....client_manager import ClientRepo
from ..common import list_active_torrents, send_menu
from ....configs import Configs


@Client.on_callback_query(custom_filters.pause_all_filter & custom_filters.check_user_filter & (custom_filters.user_is_administrator | custom_filters.user_is_manager))
async def pause_all_callback(client: Client, callback_query: CallbackQuery) -> None:
    repository = ClientRepo.get_client_manager(Configs.config.clients.type)
    repository.pause_all()
    await client.answer_callback_query(callback_query.id, "Paused all torrents")


@Client.on_callback_query(custom_filters.pause_filter & custom_filters.check_user_filter & (custom_filters.user_is_administrator | custom_filters.user_is_manager))
async def pause_callback(client: Client, callback_query: CallbackQuery) -> None:
    if callback_query.data.find("#") == -1:
        await list_active_torrents(client, 1, callback_query.from_user.id, callback_query.message.id, "pause")

    else:
        repository = ClientRepo.get_client_manager(Configs.config.clients.type)
        repository.pause(torrent_hash=callback_query.data.split("#")[1])
        await send_menu(client, callback_query.message.id, callback_query.from_user.id)
