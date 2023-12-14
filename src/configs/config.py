from pydantic import BaseModel

from .client import Client
from .user import User
from .telegram import Telegram


class MainConfig(BaseModel):
    clients: Client
    telegram: Telegram
    users: list[User]
