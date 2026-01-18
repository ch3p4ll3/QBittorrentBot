from pathlib import Path
import json

import yaml
from pydantic import BaseModel

from src.utils import inejct_new_config_data

from .client import Client
from .user import User
from .telegram import Telegram
from .redis import Redis


class Settings(BaseModel):
    client: Client
    telegram: Telegram
    users: list[User]
    redis: Redis

    def export_settings(self):
        settings_file_path = Path(__file__).parent.parent.parent / "data/config.yml"

        with open(settings_file_path, "w", encoding="UTF-8") as settings_file:
            yaml.dump(self.model_dump(mode='json'), settings_file, indent=2)
    
    def update_from(self, new: "Settings") -> None:
        for field in Settings.model_fields:
            setattr(self, field, getattr(new, field))

    @classmethod
    def load_settings(cls):
        base_path = Path(__file__).parent.parent.parent / "data"
        yml_path = base_path / "config.yml"
        json_path = base_path / "config.json"

        # If YAML config does not exist
        if not yml_path.exists():
            # If old JSON config exists, convert it
            if json_path.exists():
                with open(json_path, "r", encoding="UTF-8") as json_file:
                    json_data = json.load(json_file)

                inejct_new_config_data(json_data)

                settings = cls(**json_data)

                with open(yml_path, "w", encoding="UTF-8") as yml_file:
                    yaml.dump(settings.model_dump(mode="json"), yml_file, indent=2)

                json_path.unlink()  # delete old config.json
                return settings

            # Otherwise create default config
            settings = cls.get_default_settings()

            with open(yml_path, "w", encoding="UTF-8") as yml_file:
                yaml.dump(settings.model_dump(mode="json"), yml_file, indent=2)

            return settings

        # Load existing YAML config
        with open(yml_path, "r", encoding="UTF-8") as yml_file:
            return cls(**yaml.safe_load(yml_file))

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
            ],

            "redis": {
                "url": None
            }
        }

        return cls(**data)
