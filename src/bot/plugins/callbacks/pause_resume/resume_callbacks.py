from pyrogram import Client
from pyrogram.types import CallbackQuery

from .... import custom_filters
from .....client_manager import ClientRepo
from ...common import list_active_torrents
from .....configs import Configs
from .....configs.user import User
from .....utils import inject_user
from .....translator import Translator, Strings


@Client.on_callback_query(custom_filters.resume_all_filter & custom_filters.check_user_filter & (custom_filters.user_is_administrator | custom_filters.user_is_manager))
@inject_user
async def resume_all_callback(client: Client, callback_query: CallbackQuery, user: User) -> None:
    repository = ClientRepo.get_client_manager(Configs.config.client.type)
    repository.resume_all()
    await client.answer_callback_query(callback_query.id, Translator.translate(Strings.ResumeAllTorrents, user.locale))


@Client.on_callback_query(custom_filters.resume_filter & custom_filters.check_user_filter & (custom_filters.user_is_administrator | custom_filters.user_is_manager))
@inject_user
async def resume_callback(client: Client, callback_query: CallbackQuery, user: User) -> None:
    if callback_query.data.find("#") == -1:
        await list_active_torrents(client, callback_query.from_user.id, callback_query.message.id, "resume")

    else:
        repository = ClientRepo.get_client_manager(Configs.config.client.type)
        repository.resume(torrent_hash=callback_query.data.split("#")[1])
        await callback_query.answer(Translator.translate(Strings.ResumeTorrent, user.locale))
