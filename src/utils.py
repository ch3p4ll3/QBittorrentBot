from math import log, floor
import datetime
from typing import Dict

from aiogram import Bot

from redis_helper.wrapper import RedisWrapper
from client_manager import ClientRepo
from settings import Settings
from settings.enums import ClientTypeEnum, UserRolesEnum
from settings.user import User


async def torrent_finished(bot: Bot, redis: RedisWrapper, settings: Settings):
    repository_class = ClientRepo.get_client_manager(settings.client.type)

    for i in repository_class(settings).get_torrents(status_filter="completed"):
        if not await redis.exists(i.hash):

            for user in settings.users:
                if user.notify:
                    try:
                        await bot.send_message(user.user_id, f"torrent {i.name} has finished downloading!")
                    except:
                        pass

            await redis.set(i.hash, True, 10 * 86400)  # store for 10 days


def get_user_from_config(user_id: int, settings: Settings) -> User:
    return next(
        iter(
            [i for i in settings.users if i.user_id == user_id]
        ), None
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


def format_progress(progress: float, width: int = 20) -> str:
    """
    progress: float from 0.0 to 1.0
    """
    progress = max(0.0, min(progress, 1.0))
    filled = int(progress * width)

    bar = "█" * filled + "░" * (width - filled)
    percent = int(progress * 100)

    return f"{percent:3d}%|{bar}|\n"


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
    elif "bool" in input_type:
        return bool


def get_value(locales_dict: Dict, key_string: str) -> str:
    """Function to get value from dictionary using key strings like 'on_message.error_adding_magnet'"""
    if '.' not in key_string:
        return locales_dict[key_string]
    else:
        head, tail = key_string.split('.', 1)
        return get_value(locales_dict[head], tail)
