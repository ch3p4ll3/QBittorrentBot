from math import log, floor
import datetime
from typing import Dict

from pydantic import HttpUrl
from pyrogram.errors.exceptions import UserIsBlocked

from src import db_management
from src.client_manager import ClientRepo
from .configs import Configs
from .configs.enums import ClientTypeEnum, UserRolesEnum
from .configs.user import User


async def torrent_finished(app):
    repository = ClientRepo.get_client_manager(Configs.config.client.type)

    for i in repository.get_torrent_info(status_filter="completed"):
        if db_management.read_completed_torrents(i.hash) is None:

            for user in Configs.config.users:
                if user.notify:
                    try:
                        await app.send_message(user.user_id, f"torrent {i.name} has finished downloading!")
                    except UserIsBlocked:
                        pass
            db_management.write_completed_torrents(i.hash)


def get_user_from_config(user_id: int) -> User:
    return next(
        iter(
            [i for i in Configs.config.users if i.user_id == user_id]
        )
    )


def convert_size(size_bytes) -> str:
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(floor(log(size_bytes, 1024)))
    p = pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


def convert_eta(n) -> str:
    return str(datetime.timedelta(seconds=n))


def convert_type_from_string(input_type: str):
    if "int" in input_type:
        return int
    elif "HttpUrl" in input_type:
        return HttpUrl
    elif "ClientTypeEnum" in input_type:
        return ClientTypeEnum
    elif "UserRolesEnum" in input_type:
        return UserRolesEnum
    elif "str" in input_type:
        return str


def get_value(locales_dict: Dict, key_string: str) -> str:
    """Function to get value from dictionary using key strings like 'on_message.error_adding_magnet'"""
    if '.' not in key_string:
        return locales_dict[key_string]
    else:
        head, tail = key_string.split('.', 1)
        return get_value(locales_dict[head], tail)


def inject_user(func):
    async def wrapper(client, message):
        user = get_user_from_config(message.from_user.id)
        await func(client, message, user)
    
    return wrapper