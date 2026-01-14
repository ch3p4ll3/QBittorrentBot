from aiogram.filters import Filter
from aiogram.types import Message

from .user import GetUser, HasRole, IsAuthorizedUser


class IsCommand(Filter):
    async def __call__(self, message: Message) -> bool:
        # If the message text does NOT start with "/"
        return message.text.startswith('/')
