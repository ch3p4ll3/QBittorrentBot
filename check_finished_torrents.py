from threading import Thread
from pyrogram import Client
from pyrogram.errors.exceptions import UserIsBlocked
import time

import db_management
import qbittorrent_control
from config import AUTHORIZED_IDS, NOTIFY


class checkTorrents(Thread):
    def __init__(self, app: Client):
        Thread.__init__(self)
        self.app = app
        self.go = True

    def run(self):
        timer = time.time()
        while self.go:
            if time.time() - timer >= 60:
                self.torrent_finished()
                timer = time.time()

            if not self.go:
                break
            time.sleep(1)

    def torrent_finished(self):
        for i in qbittorrent_control.get_torrent_info():
            if i.progress == 1 and \
                    db_management.read_completed_torrents(i.hash) is None \
                    and NOTIFY:

                for user_id in AUTHORIZED_IDS:
                    try:
                        self.app.send_message(user_id, f"torrent {i.name} has finished downloading!")
                    except UserIsBlocked:
                        pass
                db_management.write_completed_torrents(i.hash)

    def stop(self):
        self.go = False
