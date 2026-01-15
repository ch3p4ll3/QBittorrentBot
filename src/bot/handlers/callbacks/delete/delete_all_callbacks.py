from aiogram import Bot, Router
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from ....filters.callbacks import DeleteMenu, Menu, DeleteOne, DeleteAll, DeleteAllData, DeleteAllNoData
from ....filters import HasRole
from client_manager import ClientRepo
from ...common import send_menu

from settings import Settings
from settings.enums import UserRolesEnum
from settings.user import User
from redis_helper.wrapper import RedisWrapper
from translator import Translator, Strings


def get_router():
    router = Router()
    
    @router.callback_query(DeleteMenu.filter(), HasRole(UserRolesEnum.Administrator))
    async def menu_delete_callback(callback_query: CallbackQuery, callback_data: DeleteMenu, bot: Bot, user: User) -> None:
        await bot.edit_message_text(
            "Delete a torrent",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text=Translator.translate(Strings.DeleteTorrentBtn, user.locale), callback_data=DeleteOne().pack())
                    ],
                    [
                        InlineKeyboardButton(text=Translator.translate(Strings.DeleteAllMenuBtn, user.locale), callback_data=DeleteAll().pack())
                    ],
                    [
                        InlineKeyboardButton(text=Translator.translate(Strings.BackToMenu, user.locale), callback_data=Menu().pack())
                    ]
                ]
            )
        )


    @router.callback_query(DeleteAll.filter(), HasRole(UserRolesEnum.Administrator))
    async def delete_all_callback(callback_query: CallbackQuery, callback_data: DeleteAll, bot: Bot, user: User) -> None:
        buttons = [
            [
                InlineKeyboardButton(text=Translator.translate(Strings.DeleteAllBtn, user.locale), callback_data=DeleteAllNoData().pack())
            ],
            [
                InlineKeyboardButton(text=Translator.translate(Strings.DeleteAllData, user.locale), callback_data=DeleteAllData().pack())
            ],
            [
                InlineKeyboardButton(text=Translator.translate(Strings.BackToMenu, user.locale), callback_data=Menu().pack())
            ]
        ]

        await bot.edit_message_reply_markup(
            callback_query.from_user.id,
            callback_query.message.message_id,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
        )


    @router.callback_query(DeleteAllNoData.filter(), HasRole(UserRolesEnum.Administrator))
    async def delete_all_with_no_data_callback(callback_query: CallbackQuery, callback_data: DeleteAllNoData, bot: Bot, settings: Settings, redis: RedisWrapper, user: User) -> None:
        repository_class = ClientRepo.get_client_manager(settings.client.type)
        repository_class(settings).delete_all_no_data()

        await bot.answer_callback_query(callback_query.id, Translator.translate(Strings.DeletedAll, user.locale))
        await send_menu(bot, redis, settings, callback_query.from_user.id, callback_query.message.message_id)


    @router.callback_query(DeleteAllData.filter(), HasRole(UserRolesEnum.Administrator))
    async def delete_all_with_data_callback(callback_query: CallbackQuery, callback_data: DeleteAllData, bot: Bot, settings: Settings, redis: RedisWrapper, user: User) -> None:
        repository_class = ClientRepo.get_client_manager(settings.client.type)
        repository_class(settings).delete_all_data()

        await bot.answer_callback_query(callback_query.id, Translator.translate(Strings.DeletedAllData, user.locale))
        await send_menu(bot, redis, settings, callback_query.from_user.id, callback_query.message.message_id)

    return router
