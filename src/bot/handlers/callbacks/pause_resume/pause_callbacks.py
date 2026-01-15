from aiogram import Bot, Router
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from ....filters.callbacks import PauseResumeMenu, Menu, PauseAll, Pause, Resume, ResumeAll
from ....filters import HasRole
from client_manager import ClientRepo
from ...common import list_active_torrents

from settings import Settings
from settings.enums import UserRolesEnum
from settings.user import User

from translator import Translator, Strings


def get_router():
    router = Router()

    @router.callback_query(PauseResumeMenu.filter(), HasRole(UserRolesEnum.Administrator))
    async def menu_pause_resume_callback(callback_query: CallbackQuery, callback_data: PauseResumeMenu, bot: Bot, user: User) -> None:
        await bot.edit_message_text(
            chat_id=callback_query.from_user.id,
            message_id=callback_query.message.message_id,
            text=Translator.translate(Strings.PauseResumeMenu, user.locale),
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text=Translator.translate(Strings.PauseTorrentBtn, user.locale), callback_data=Pause(torrent_hash="").pack()),
                        InlineKeyboardButton(text=Translator.translate(Strings.ResumeTorrentBtn, user.locale), callback_data=Resume(torrent_hash="").pack())
                    ],
                    [
                        InlineKeyboardButton(text=Translator.translate(Strings.PauseAll, user.locale), callback_data=PauseAll().pack()),
                        InlineKeyboardButton(text=Translator.translate(Strings.ResumeAll, user.locale), callback_data=ResumeAll().pack())
                    ],
                    [
                        InlineKeyboardButton(text=Translator.translate(Strings.BackToMenu, user.locale), callback_data=Menu().pack())
                    ]
                ]
            )
        )


    @router.callback_query(PauseAll.filter(), HasRole(UserRolesEnum.Administrator))
    @router.callback_query(PauseAll.filter(), HasRole(UserRolesEnum.Manager))
    async def pause_all_callback(callback_query: CallbackQuery, callback_data: PauseAll, bot: Bot, settings: Settings, user: User) -> None:
        repository_class = ClientRepo.get_client_manager(settings.client.type)
        repository_class(settings).pause_all()
        
        await callback_query.answer(
            text=Translator.translate(Strings.PauseAllTorrents,user.locale)
        )


    @router.callback_query(Pause.filter(), HasRole(UserRolesEnum.Administrator))
    @router.callback_query(Pause.filter(), HasRole(UserRolesEnum.Manager))
    async def pause_callback(callback_query: CallbackQuery, callback_data: Pause, bot: Bot, settings: Settings, user: User) -> None:
        if not callback_data.torrent_hash:
            await list_active_torrents(bot, callback_query.from_user.id, callback_query.message.message_id, settings, callback="pause")

        else:
            repository_class = ClientRepo.get_client_manager(settings.client.type)
            repository_class(settings).pause(torrent_hash=callback_data.torrent_hash)
            await callback_query.answer(text=Translator.translate(Strings.PauseTorrent, user.locale))

    return router