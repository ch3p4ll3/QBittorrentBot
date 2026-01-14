from pyrogram import Client
from pyrogram.types import CallbackQuery

from ....filters import custom_filters
from .....client_manager import ClientRepo
from ...common import list_active_torrents
from .....settings import Configs
from .....settings.user import User
from .....utils import inject_user
from .....translator import Translator, Strings


@Client.on_callback_query(custom_filters.pause_all_filter & custom_filters.check_user_filter & (custom_filters.user_is_administrator | custom_filters.user_is_manager))
@inject_user
async def pause_all_callback(client: Client, callback_query: CallbackQuery, user: User) -> None:
    repository = ClientRepo.get_client_manager(Configs.config.client.type)
    repository.pause_all()
    await client.answer_callback_query(callback_query.id, Translator.translate(Strings.PauseAllTorrents, user.locale))


@Client.on_callback_query(custom_filters.pause_filter & custom_filters.check_user_filter & (custom_filters.user_is_administrator | custom_filters.user_is_manager))
@inject_user
async def pause_callback(client: Client, callback_query: CallbackQuery, user: User) -> None:
    if callback_query.data.find("#") == -1:
        await list_active_torrents(client, callback_query.from_user.id, callback_query.message.id, "pause")

    else:
        repository = ClientRepo.get_client_manager(Configs.config.client.type)
        repository.pause(torrent_hash=callback_query.data.split("#")[1])
        await callback_query.answer(Translator.translate(Strings.PauseTorrent, user.locale))
