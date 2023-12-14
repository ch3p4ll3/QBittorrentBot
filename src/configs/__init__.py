from .config import MainConfig
from os import getenv
from json import load
from typing import Union


class Configs:
    config_path = f'{ "/app/config/" if getenv("IS_DOCKER", False) else "./"}config.json'

    @classmethod
    def load_config(cls) -> Union[MainConfig, None]:
        with open(cls.config_path, 'r') as config_json:
            configs = MainConfig(**(load(config_json)))

        return configs

    @classmethod
    def update_config(cls, edited_config: MainConfig) -> Union[MainConfig, None]:
        # TODO: update config from bot
        pass
