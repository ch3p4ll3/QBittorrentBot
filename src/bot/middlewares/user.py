from typing import Dict, Any

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message

from utils import get_user_from_config
from settings import Settings


class UserMiddleware(BaseMiddleware):
    def __init__(self, settings: Settings):
        super().__init__()
        self.settings = settings

    async def __call__(self, handler, event, data: Dict[str, Any]):
        """
        This method is called for each incoming event. It will check if it's a message or callback query
        and inject the user accordingly.
        """
        if isinstance(event, Message):
            # Handle message event (e.g., log message, inject user data, etc.)
            data['user'] = get_user_from_config(event.from_user.id, self.settings)

        elif isinstance(event, CallbackQuery):
            # Handle callback query event (e.g., log callback, inject user data, etc.)
            data['user'] = get_user_from_config(event.from_user.id, self.settings)

        # Continue to the handler
        return await handler(event, data)
