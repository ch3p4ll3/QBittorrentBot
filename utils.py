from math import log, floor
import datetime
from pyrogram.errors.exceptions import UserIsBlocked

import db_management
import qbittorrent_control
from config import AUTHORIZED_IDS, NOTIFY


async def torrent_finished(app):
    for i in qbittorrent_control.get_torrent_info():
        if i.progress == 1 and \
                db_management.read_completed_torrents(i.hash) is None \
                and NOTIFY:

            for user_id in AUTHORIZED_IDS:
                try:
                    await app.send_message(user_id, f"torrent {i.name} has finished downloading!")
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
