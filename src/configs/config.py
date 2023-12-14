from pydantic import BaseModel

from .client import Client
from .users import Users
from .telegram import Telegram


class MainConfig(BaseModel):
    clients: Client
    telegram: Telegram
    users: list[Users]
