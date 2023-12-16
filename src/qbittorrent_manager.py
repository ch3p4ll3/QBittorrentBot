import qbittorrentapi
import logging
from .configs import Configs
from typing import Union, List

BOT_CONFIGS = Configs.config
logger = logging.getLogger(__name__)


class QbittorrentManagement:
    def __init__(self):
        self.qbt_client = qbittorrentapi.Client(**BOT_CONFIGS.clients.connection_string)

    def __enter__(self):
        try:
            self.qbt_client.auth_log_in()
        except qbittorrentapi.LoginFailed as e:
            logger.exception("Qbittorrent Login Failed", exc_info=True)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.qbt_client.auth_log_out()

    def add_magnet(self, magnet_link: Union[str, List[str]], category: str = None) -> None:
        if category == "None":
            category = None

        if category is not None:
            logger.debug(f"Adding magnet with category {category}")
            self.qbt_client.torrents_add(urls=magnet_link, category=category)
        else:
            logger.debug("Adding magnet without category")
            self.qbt_client.torrents_add(urls=magnet_link)

    def add_torrent(self, file_name: str, category: str = None) -> None:
        if category == "None":
            category = None

        try:
            if category is not None:
                logger.debug(f"Adding torrent with category {category}")
                self.qbt_client.torrents_add(torrent_files=file_name, category=category)
            else:
                logger.debug("Adding torrent without category")
                self.qbt_client.torrents_add(torrent_files=file_name)

        except qbittorrentapi.exceptions.UnsupportedMediaType415Error:
            pass

    def resume_all(self) -> None:
        logger.debug("Resuming all torrents")
        self.qbt_client.torrents.resume.all()

    def pause_all(self) -> None:
        logger.debug("Pausing all torrents")
        self.qbt_client.torrents.pause.all()

    def resume(self, torrent_hash: str) -> None:
        logger.debug(f"Resuming torrent with has {torrent_hash}")
        self.qbt_client.torrents_resume(torrent_hashes=torrent_hash)

    def pause(self, torrent_hash: str) -> None:
        logger.debug(f"Pausing torrent with hash {torrent_hash}")
        self.qbt_client.torrents_pause(torrent_hashes=torrent_hash)

    def delete_one_no_data(self, torrent_hash: str) -> None:
        logger.debug(f"Deleting torrent with hash {torrent_hash} without removing files")
        self.qbt_client.torrents_delete(delete_files=False,
                                        torrent_hashes=torrent_hash)

    def delete_one_data(self, torrent_hash: str) -> None:
        logger.debug(f"Deleting torrent with hash {torrent_hash} + removing files")
        self.qbt_client.torrents_delete(delete_files=True,
                                        torrent_hashes=torrent_hash)

    def delete_all_no_data(self) -> None:
        logger.debug(f"Deleting all torrents")
        for i in self.qbt_client.torrents_info():
            self.qbt_client.torrents_delete(delete_files=False, hashes=i.hash)

    def delete_all_data(self) -> None:
        logger.debug(f"Deleting all torrent + files")
        for i in self.qbt_client.torrents_info():
            self.qbt_client.torrents_delete(delete_files=True, hashes=i.hash)

    def get_categories(self):
        categories = self.qbt_client.torrent_categories.categories
        if len(categories) > 0:
            return categories

        else:
            return

    def get_torrent_info(self, torrent_hash: str = None, status_filter: str = None):
        if torrent_hash is None:
            logger.debug("Getting torrents infos")
            return self.qbt_client.torrents_info(status_filter=status_filter)
        logger.debug(f"Getting infos for torrent with hash {torrent_hash}")
        return next(iter(self.qbt_client.torrents_info(status_filter=status_filter, torrent_hashes=torrent_hash)), None)

    def edit_category(self, name: str, save_path: str) -> None:
        logger.debug(f"Editing category {name}, new save path: {save_path}")
        self.qbt_client.torrents_edit_category(name=name,
                                               save_path=save_path)

    def create_category(self, name: str, save_path: str) -> None:
        logger.debug(f"Creating new category {name} with save path: {save_path}")
        self.qbt_client.torrents_create_category(name=name,
                                                 save_path=save_path)

    def remove_category(self, name: str) -> None:
        logger.debug(f"Removing category {name}")
        self.qbt_client.torrents_remove_categories(categories=name)
