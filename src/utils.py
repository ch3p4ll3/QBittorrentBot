from math import log, floor
import datetime
from typing import Dict

from src.settings.user import User


def get_user_from_config(user_id: int, settings: "Settings") -> User:
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


def get_value(locales_dict: Dict, key_string: str) -> str:
    """Function to get value from dictionary using key strings like 'on_message.error_adding_magnet'"""
    if '.' not in key_string:
        return locales_dict[key_string]
    else:
        head, tail = key_string.split('.', 1)
        return get_value(locales_dict[head], tail)


def inejct_new_config_data(json_data: dict):
    json_data['redis'] = {
        'url': None
    }

    for index, i in enumerate(json_data['users']):
        i['notification_filter'] = []
        json_data['users'][index] = i
