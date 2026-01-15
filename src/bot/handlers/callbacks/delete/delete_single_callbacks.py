from aiogram import Bot, Router
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from ....filters.callbacks import DeleteOne, Menu, DeleteOneData, DeleteOneNoData
from ....filters import HasRole
from client_manager import ClientRepo
from ...common import send_menu, list_active_torrents

from settings import Settings
from settings.enums import UserRolesEnum
from settings.user import User
from redis_helper.wrapper import RedisWrapper
from translator import Translator, Strings


def get_router():
    router = Router()

    @router.callback_query(DeleteOne.filter(), HasRole(UserRolesEnum.Administrator))
    async def delete_callback(callback_query: CallbackQuery, callback_data: DeleteOne, bot: Bot, settings: Settings, user: User) -> None:
        if not callback_data.torrent_hash:
            await list_active_torrents(bot, callback_query.from_user.id, callback_query.message.message_id, settings, "delete_one")

        else:
            buttons = [
                [
                    InlineKeyboardButton(text=Translator.translate(Strings.DeleteSingleBtn, user.locale), callback_data=DeleteOneNoData(torrent_hash=callback_data.torrent_hash).pack())
                ],
                [
                    InlineKeyboardButton(text=Translator.translate(Strings.DeleteSingleDataBtn, user.locale), callback_data=DeleteOneData(torrent_hash=callback_data.torrent_hash).pack())
                ],
                [
                    InlineKeyboardButton(text=Translator.translate(Strings.BackToMenu, user.locale), callback_data=Menu().pack())
                ]
            ]

            await bot.edit_message_reply_markup(
                chat_id=callback_query.from_user.id,
                message_id=callback_query.message.message_id,
                reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
            )


    @router.callback_query(DeleteOneNoData.filter(), HasRole(UserRolesEnum.Administrator))
    async def delete_no_data_callback(callback_query: CallbackQuery, callback_data: DeleteOneNoData, bot: Bot, settings: Settings, redis: RedisWrapper, user: User) -> None:
        if not callback_data.torrent_hash:
            await list_active_torrents(bot, callback_query.from_user.id, callback_query.message.message_id, settings, "delete_one_no_data")

        else:
            repository_class = ClientRepo.get_client_manager(settings.client.type)
            repository_class(settings).delete_one_no_data(torrent_hash=callback_data.torrent_hash)

            await send_menu(bot, redis, settings, callback_query.from_user.id, callback_query.message.message_id)


    @router.callback_query(DeleteOneData.filter(), HasRole(UserRolesEnum.Administrator))
    async def delete_with_data_callback(callback_query: CallbackQuery, callback_data: DeleteOneData, bot: Bot, settings: Settings, redis: RedisWrapper, user: User) -> None:
        if not callback_data.torrent_hash:
            await list_active_torrents(bot, callback_query.from_user.id, callback_query.message.message_id, settings, "delete_one_data")

        else:
            repository_class = ClientRepo.get_client_manager(settings.client.type)
            repository_class(settings).delete_one_data(torrent_hash=callback_data.torrent_hash)

            await send_menu(bot, redis, settings, callback_query.from_user.id, callback_query.message.message_id)

    return router
