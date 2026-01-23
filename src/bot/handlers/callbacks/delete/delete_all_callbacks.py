from aiogram import Bot, Router
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.utils.i18n import gettext as _

from src.bot.filters.callbacks import DeleteMenu, Menu, DeleteOne, DeleteAll, DeleteAllData, DeleteAllNoData
from src.bot.filters import HasRole
from src.client_manager.client_repo import ClientRepo
from src.bot.handlers.common import send_menu

from src.settings import Settings
from src.settings.enums import UserRolesEnum
from src.settings.user import User
from src.redis_helper.wrapper import RedisWrapper


def get_router():
    router = Router()

    @router.callback_query(DeleteMenu.filter(), HasRole(UserRolesEnum.Administrator))
    async def menu_delete_callback(callback_query: CallbackQuery, callback_data: DeleteMenu, bot: Bot, user: User) -> None:
        await bot.edit_message_text(
            chat_id=callback_query.from_user.id,
            message_id=callback_query.message.message_id,
            text="Delete a torrent",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text=_("🗑 Delete"), callback_data=DeleteOne(torrent_hash="").pack())
                    ],
                    [
                        InlineKeyboardButton(text=_("🗑 Delete All"), callback_data=DeleteAll().pack())
                    ],
                    [
                        InlineKeyboardButton(text=_("🔙 Menu"), callback_data=Menu().pack())
                    ]
                ]
            )
        )


    @router.callback_query(DeleteAll.filter(), HasRole(UserRolesEnum.Administrator))
    async def delete_all_callback(callback_query: CallbackQuery, callback_data: DeleteAll, bot: Bot, user: User) -> None:
        buttons = [
            [
                InlineKeyboardButton(text=_("🗑 Delete all torrents"), callback_data=DeleteAllNoData().pack())
            ],
            [
                InlineKeyboardButton(text=_("🗑 Delete all torrents and data"), callback_data=DeleteAllData().pack())
            ],
            [
                InlineKeyboardButton(text=_("🔙 Menu"), callback_data=Menu().pack())
            ]
        ]

        await bot.edit_message_reply_markup(
            chat_id=callback_query.from_user.id,
            message_id=callback_query.message.message_id,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
        )


    @router.callback_query(DeleteAllNoData.filter(), HasRole(UserRolesEnum.Administrator))
    async def delete_all_with_no_data_callback(callback_query: CallbackQuery, callback_data: DeleteAllNoData, bot: Bot, settings: Settings, redis: RedisWrapper, user: User) -> None:
        repository_class = ClientRepo.get_client_manager(settings.client.type)
        await repository_class(settings).delete_all_no_data()

        await bot.answer_callback_query(callback_query.id, _("Deleted all torrents"))
        await send_menu(bot, redis, settings, callback_query.from_user.id, callback_query.message.message_id)


    @router.callback_query(DeleteAllData.filter(), HasRole(UserRolesEnum.Administrator))
    async def delete_all_with_data_callback(callback_query: CallbackQuery, callback_data: DeleteAllData, bot: Bot, settings: Settings, redis: RedisWrapper, user: User) -> None:
        repository_class = ClientRepo.get_client_manager(settings.client.type)
        await repository_class(settings).delete_all_data()

        await bot.answer_callback_query(callback_query.id, _("Deleted all torrents and data"))
        await send_menu(bot, redis, settings, callback_query.from_user.id, callback_query.message.message_id)

    return router
