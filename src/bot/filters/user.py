from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery

from src.settings import Settings
from src.settings.enums import UserRolesEnum
from src.utils import get_user_from_config


# Authorization filters
class IsAuthorizedUser(Filter):
    async def __call__(self, message: Message, settings: Settings) -> bool:
        allowed_ids = {i.user_id for i in settings.users}

        return message.from_user.id in allowed_ids


class GetUser(Filter):
    async def __call__(self, message: Message, settings: Settings) -> bool:
        allowed_ids = {i.user_id for i in settings.users}

        if message.from_user.id in allowed_ids:
            return {'user': get_user_from_config(message.from_user.id, settings)}

        return None


class HasRole(Filter):
    def __init__(self, role: UserRolesEnum):
        self.role = role

    async def __call__(self, query: CallbackQuery, settings: Settings) -> bool:
        user = get_user_from_config(query.from_user.id, settings)
        return user and user.role == self.role