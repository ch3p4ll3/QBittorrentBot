from aiogram import Bot, Router
from aiogram.types import CallbackQuery

from ...filters.callbacks import List, ListByStatus, Menu
from ..common import list_active_torrents, send_menu
from settings import Settings
from redis_helper.wrapper import RedisWrapper


def get_router():
    router = Router()

    @router.callback_query(List.filter())
    async def list_callback(callback_query: CallbackQuery, callback_data: List, settings: Settings, bot: Bot) -> None:
        await list_active_torrents(bot, callback_query.from_user.id, callback_query.message.message_id, settings)


    @router.callback_query(ListByStatus.filter())
    async def list_by_status_callback(callback_query: CallbackQuery, callback_data: ListByStatus, settings: Settings, bot: Bot) -> None:
        status_filter = callback_data.status
        await list_active_torrents(bot, callback_query.from_user.id, callback_query.message.message_id, settings, status_filter=status_filter)


    @router.callback_query(Menu.filter())
    async def menu_callback(callback_query: CallbackQuery, callback_data: Menu, bot: Bot, redis: RedisWrapper, settings: Settings) -> None:
        await send_menu(bot, redis, settings, callback_query.from_user.id, callback_query.message.message_id)

    return router
