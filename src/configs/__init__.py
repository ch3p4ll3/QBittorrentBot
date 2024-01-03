from .config import MainConfig
from os import getenv
from json import load
from typing import Union


config_path = f'{ "/app/config/" if getenv("IS_DOCKER", False) else "./"}config.json'


def load_config() -> Union[MainConfig, None, int]:
    with open(config_path, 'r') as config_json:
        configs = MainConfig(**(load(config_json)))

    return configs


class Configs:
    config_path = config_path
    log_folder = "/app/config/logs" if getenv("IS_DOCKER", False) else "./logs"
    config = load_config()

    @classmethod
    def reload_config(cls) -> Union[MainConfig, None, int]:
        with open(cls.config_path, 'r') as config_json:
            cls.config = MainConfig(**(load(config_json)))

        return cls.config

    @classmethod
    def update_config(cls, edited_config: MainConfig) -> Union[MainConfig, None]:
        # TODO: update config from bot
        with open(cls.config_path, "w") as json_file:
            json_file.write(
                edited_config.model_dump_json(indent=4)
            )
        return edited_config
