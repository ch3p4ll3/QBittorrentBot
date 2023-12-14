from .config import MainConfig
from os import getenv
from json import load
from typing import Union


class Configs:
    @classmethod
    def load_config(cls) -> Union[MainConfig, None]:
        with open(f'{ "/app/config/" if getenv("IS_DOCKER", False) else "./"}config.json', 'r') as config_json:
            configs = MainConfig(**(load(config_json)))

        return configs

    @classmethod
    def update_config(cls, edited_config: MainConfig) -> Union[MainConfig, None]:
        # TODO: update config from bot
        pass
