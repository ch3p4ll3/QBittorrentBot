from pathlib import Path

from pydantic import BaseModel
from yaml import safe_load, dump

from .client import Client
from .user import User
from .telegram import Telegram


class Settings(BaseModel):
    client: Client
    telegram: Telegram
    users: list[User]

    def export_settings(self):
        settings_file_path = Path(__file__).parent.parent / "data/config.yml"

        with open(settings_file_path, "w") as settings_file:
            dump(self.model_dump(mode='json'), settings_file, indent=2)

    @classmethod
    def load_settings(cls):
        settings_file_path = Path(__file__).parent.parent / "data/config.yml"

        if not settings_file_path.exists():
            settings = cls.get_default_settings()

            with open(settings_file_path, "w") as settings_file:
                dump(settings.model_dump(mode='json'), settings_file, indent=2)

            return settings

        with open(settings_file_path, "r") as settings_file:
            return cls(**safe_load(settings_file))

    @classmethod
    def get_default_settings(cls):
        data = {
            "client": {
                "type": "qbittorrent",
                "host": "http://localhost:8080",
                "user": "admin",
                "password": "adminadmin"
            },
            "telegram": {
                "bot_token": "PUT_YOUR_TELEGRAM_BOT_TOKEN_HERE",
                "proxy": None
            },
            "users": [
                {
                "user_id": 123456789,
                "role": "administrator",
                "locale": "en",
                "notify": True
                }
            ]
        }


        return cls(**data)