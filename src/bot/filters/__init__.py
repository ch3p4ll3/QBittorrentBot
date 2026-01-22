from aiogram.filters import Filter
from aiogram.types import Message

from .user import GetUser, HasRole, IsAuthorizedUser    # noqa: F401


class IsCommand(Filter):
    async def __call__(self, message: Message) -> bool:
        # If the message text does NOT start with "/"
        if message.text:
            return message.text.startswith('/')
        else:
            return False
