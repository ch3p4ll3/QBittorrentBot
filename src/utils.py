from math import log, floor
import datetime
from pyrogram.errors.exceptions import UserIsBlocked

from src import db_management
from src.qbittorrent_manager import QbittorrentManagement
from .configs import Configs


BOT_CONFIGS = Configs.load_config()


async def torrent_finished(app):
    with QbittorrentManagement() as qb:
        for i in qb.get_torrent_info(status_filter="completed"):
            if db_management.read_completed_torrents(i.hash) is None:

                for user in BOT_CONFIGS.users:
                    if user.notify:
                        try:
                            await app.send_message(user.user_id, f"torrent {i.name} has finished downloading!")
                        except UserIsBlocked:
                            pass
                db_management.write_completed_torrents(i.hash)


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
