from pydantic import BaseModel
from typing import Optional

from .client import Client
from .user import User
from .telegram import Telegram
from .logger import Logger


class MainConfig(BaseModel):
    client: Client
    telegram: Telegram
    users: list[User]
    logger: Logger
