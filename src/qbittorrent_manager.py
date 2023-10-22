import qbittorrentapi
from src.config import BOT_CONFIGS

from typing import Union, List


class QbittorrentManagement:
    def __init__(self):
        self.qbt_client = qbittorrentapi.Client(
            host=f'http://{BOT_CONFIGS.qbittorrent.ip.network_address}:'
                 f'{BOT_CONFIGS.qbittorrent.port}',
            username=BOT_CONFIGS.qbittorrent.user,
            password=BOT_CONFIGS.qbittorrent.password)

    def __enter__(self):
        try:
            self.qbt_client.auth_log_in()
        except qbittorrentapi.LoginFailed as e:
            print(e)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.qbt_client.auth_log_out()

    def add_magnet(self, magnet_link: Union[str, List[str]], category: str = None) -> None:
        if category == "None":
            category = None

        if category is not None:
            self.qbt_client.torrents_add(urls=magnet_link, category=category)
        else:
            self.qbt_client.torrents_add(urls=magnet_link)

    def add_torrent(self, file_name: str, category: str = None) -> None:
        if category == "None":
            category = None

        try:
            if category is not None:
                self.qbt_client.torrents_add(torrent_files=file_name, category=category)
            else:
                self.qbt_client.torrents_add(torrent_files=file_name)

        except qbittorrentapi.exceptions.UnsupportedMediaType415Error:
            pass

    def resume_all(self) -> None:
        self.qbt_client.torrents.resume.all()

    def pause_all(self) -> None:
        self.qbt_client.torrents.pause.all()

    def resume(self, torrent_hash: str) -> None:
        self.qbt_client.torrents_resume(torrent_hashes=torrent_hash)

    def pause(self, torrent_hash: str) -> None:
        self.qbt_client.torrents_pause(torrent_hashes=torrent_hash)

    def delete_one_no_data(self, torrent_hash: str) -> None:
        self.qbt_client.torrents_delete(delete_files=False,
                                        torrent_hashes=torrent_hash)

    def delete_one_data(self, torrent_hash: str) -> None:
        self.qbt_client.torrents_delete(delete_files=True,
                                        torrent_hashes=torrent_hash)

    def delete_all_no_data(self) -> None:
        for i in self.qbt_client.torrents_info():
            self.qbt_client.torrents_delete(delete_files=False, hashes=i.hash)

    def delete_all_data(self) -> None:
        for i in self.qbt_client.torrents_info():
            self.qbt_client.torrents_delete(delete_files=True, hashes=i.hash)

    def get_categories(self):
        categories = self.qbt_client.torrent_categories.categories
        if len(categories) > 0:
            return categories

        else:
            return

    def get_torrent_info(self, data: str = None, status_filter: str = None, ):
        if data is None:
            return self.qbt_client.torrents_info(status_filter=status_filter)
        return next(iter(self.qbt_client.torrents_info(status_filter=status_filter, torrent_hashes=data)), None)

    def edit_category(self, name: str, save_path: str) -> None:
        self.qbt_client.torrents_edit_category(name=name,
                                               save_path=save_path)

    def create_category(self, name: str, save_path: str) -> None:
        self.qbt_client.torrents_create_category(name=name,
                                                 save_path=save_path)

    def remove_category(self, data: str) -> None:
        self.qbt_client.torrents_remove_categories(categories=data)
