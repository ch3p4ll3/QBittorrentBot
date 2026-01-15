from aiogram import Bot, Router
from aiogram.types import CallbackQuery

from ....filters.callbacks import Resume, ResumeAll
from ....filters import HasRole
from client_manager import ClientRepo
from ...common import list_active_torrents

from settings import Settings
from settings.enums import UserRolesEnum
from settings.user import User

from translator import Translator, Strings


def get_router():
    router = Router()

    @router.callback_query(ResumeAll.filter(), HasRole(UserRolesEnum.Administrator))
    @router.callback_query(ResumeAll.filter(), HasRole(UserRolesEnum.Manager))
    async def resume_all_callback(callback_query: CallbackQuery, callback_data: ResumeAll, bot: Bot, settings: Settings, user: User) -> None:
        repository_class = ClientRepo.get_client_manager(settings.client.type)
        repository_class(settings).resume_all()

        await bot.answer_callback_query(
            callback_query.id,
            Translator.translate(Strings.ResumeAllTorrents, user.locale)
        )


    @router.callback_query(Resume.filter(), HasRole(UserRolesEnum.Administrator))
    @router.callback_query(Resume.filter(), HasRole(UserRolesEnum.Manager))
    async def resume_callback(callback_query: CallbackQuery, callback_data: Resume, bot: Bot, settings: Settings, user: User) -> None:
        if not callback_data.torrent_hash:
            await list_active_torrents(bot, callback_query.from_user.id, callback_query.message.message_id, settings, callback="resume")

        else:
            repository_class = ClientRepo.get_client_manager(settings.client.type)
            repository_class(settings).resume(torrent_hash=callback_data.torrent_hash)

            await callback_query.answer(Translator.translate(Strings.ResumeTorrent, user.locale))

    return router
