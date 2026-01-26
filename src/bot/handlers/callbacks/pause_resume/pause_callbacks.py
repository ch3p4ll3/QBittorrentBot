from aiogram import Bot, Router
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.utils.i18n import gettext as _

from src.bot.filters.callbacks import PauseResumeMenu, Menu, PauseAll, Pause, Resume, ResumeAll
from src.bot.filters import HasRole
from src.client_manager.client_repo import ClientRepo
from src.bot.handlers.common import list_active_torrents

from src.settings import Settings
from src.settings.enums import UserRolesEnum


def get_router():
    router = Router()

    @router.callback_query(PauseResumeMenu.filter(), HasRole(UserRolesEnum.Administrator))
    async def menu_pause_resume_callback(callback_query: CallbackQuery, callback_data: PauseResumeMenu, bot: Bot) -> None:
        await bot.edit_message_text(
            chat_id=callback_query.from_user.id,
            message_id=callback_query.message.message_id,
            text=_("Pause/Resume a torrent"),
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text=_("⏸ Pause"), callback_data=Pause(torrent_hash="").pack()),
                        InlineKeyboardButton(text=_("▶️ Resume"), callback_data=Resume(torrent_hash="").pack())
                    ],
                    [
                        InlineKeyboardButton(text=_("⏸ Pause All"), callback_data=PauseAll().pack()),
                        InlineKeyboardButton(text=_("▶\uFE0F Resume All"), callback_data=ResumeAll().pack())
                    ],
                    [
                        InlineKeyboardButton(text=_("🔙 Menu"), callback_data=Menu().pack())
                    ]
                ]
            )
        )


    @router.callback_query(PauseAll.filter(), HasRole(UserRolesEnum.Administrator))
    @router.callback_query(PauseAll.filter(), HasRole(UserRolesEnum.Manager))
    async def pause_all_callback(callback_query: CallbackQuery, callback_data: PauseAll, bot: Bot, settings: Settings) -> None:
        repository_class = ClientRepo.get_client_manager(settings.client.type)
        await repository_class(settings).pause_all()

        await callback_query.answer(
            text=_("Paused all torrents")
        )


    @router.callback_query(Pause.filter(), HasRole(UserRolesEnum.Administrator))
    @router.callback_query(Pause.filter(), HasRole(UserRolesEnum.Manager))
    async def pause_callback(callback_query: CallbackQuery, callback_data: Pause, bot: Bot, settings: Settings) -> None:
        if not callback_data.torrent_hash:
            await list_active_torrents(bot, callback_query.from_user.id, callback_query.message.message_id, settings, callback="pause")

        else:
            repository_class = ClientRepo.get_client_manager(settings.client.type)
            await repository_class(settings).pause(torrent_hash=callback_data.torrent_hash)
            await callback_query.answer(text=_("Torrent Paused"))

    return router
