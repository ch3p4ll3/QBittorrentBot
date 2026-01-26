from aiogram import Bot, Router
from aiogram.types import CallbackQuery
from aiogram.utils.i18n import gettext as _

from src.settings.user import User
from src.settings.enums import UserRolesEnum

from src.bot.filters import HasRole
from src.bot.filters.callbacks import AddMagnet, AddTorrent

from src.redis_helper.wrapper import RedisWrapper


def get_router():
    router = Router()

    @router.callback_query(AddMagnet.filter(), HasRole(UserRolesEnum.Administrator))
    @router.callback_query(AddMagnet.filter(), HasRole(UserRolesEnum.Manager))
    async def add_magnet_callback(callback_query: CallbackQuery, callback_data: AddMagnet, bot: Bot, redis: RedisWrapper, user: User) -> None:
        print(callback_data.pack())
        await redis.set(f"action:{callback_query.from_user.id}", f"magnet#{callback_data.category}")
        await bot.answer_callback_query(callback_query.id, _("Send a magnet link"))


    @router.callback_query(AddTorrent.filter(), HasRole(UserRolesEnum.Administrator))
    @router.callback_query(AddTorrent.filter(), HasRole(UserRolesEnum.Manager))
    async def add_torrent_callback(callback_query: CallbackQuery, callback_data: AddTorrent, bot: Bot, redis: RedisWrapper, user: User) -> None:
        await redis.set(f"action:{callback_query.from_user.id}", f"torrent#{callback_data.category}")
        await bot.answer_callback_query(callback_query.id, _("Send a torrent file"))

    return router
