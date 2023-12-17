import qbittorrentapi
import logging
from src.configs import Configs
from typing import Union, List
from .client_manager import ClientManager

BOT_CONFIGS = Configs.config
logger = logging.getLogger(__name__)


class QbittorrentManager(ClientManager):
    @classmethod
    def add_magnet(cls, magnet_link: Union[str, List[str]], category: str = None) -> None:
        if category == "None":
            category = None

        with qbittorrentapi.Client(**BOT_CONFIGS.clients.connection_string) as qbt_client:
            logger.debug(f"Adding magnet with category {category}")
            qbt_client.torrents_add(urls=magnet_link, category=category)

    @classmethod
    def add_torrent(cls, file_name: str, category: str = None) -> None:
        if category == "None":
            category = None

        try:
            with qbittorrentapi.Client(**BOT_CONFIGS.clients.connection_string) as qbt_client:
                logger.debug(f"Adding torrent with category {category}")
                qbt_client.torrents_add(torrent_files=file_name, category=category)

        except qbittorrentapi.exceptions.UnsupportedMediaType415Error:
            pass

    @classmethod
    def resume_all(cls) -> None:
        logger.debug("Resuming all torrents")
        with qbittorrentapi.Client(**BOT_CONFIGS.clients.connection_string) as qbt_client:
            qbt_client.torrents.resume.all()

    @classmethod
    def pause_all(cls) -> None:
        logger.debug("Pausing all torrents")
        with qbittorrentapi.Client(**BOT_CONFIGS.clients.connection_string) as qbt_client:
            qbt_client.torrents.pause.all()

    @classmethod
    def resume(cls, torrent_hash: str) -> None:
        logger.debug(f"Resuming torrent with has {torrent_hash}")
        with qbittorrentapi.Client(**BOT_CONFIGS.clients.connection_string) as qbt_client:
            qbt_client.torrents_resume(torrent_hashes=torrent_hash)

    @classmethod
    def pause(cls, torrent_hash: str) -> None:
        logger.debug(f"Pausing torrent with hash {torrent_hash}")
        with qbittorrentapi.Client(**BOT_CONFIGS.clients.connection_string) as qbt_client:
            qbt_client.torrents_pause(torrent_hashes=torrent_hash)

    @classmethod
    def delete_one_no_data(cls, torrent_hash: str) -> None:
        logger.debug(f"Deleting torrent with hash {torrent_hash} without removing files")
        with qbittorrentapi.Client(**BOT_CONFIGS.clients.connection_string) as qbt_client:
            qbt_client.torrents_delete(
                delete_files=False,
                torrent_hashes=torrent_hash
            )

    @classmethod
    def delete_one_data(cls, torrent_hash: str) -> None:
        logger.debug(f"Deleting torrent with hash {torrent_hash} + removing files")
        with qbittorrentapi.Client(**BOT_CONFIGS.clients.connection_string) as qbt_client:
            qbt_client.torrents_delete(
                delete_files=True,
                torrent_hashes=torrent_hash
            )

    @classmethod
    def delete_all_no_data(cls) -> None:
        logger.debug(f"Deleting all torrents")
        with qbittorrentapi.Client(**BOT_CONFIGS.clients.connection_string) as qbt_client:
            for i in qbt_client.torrents_info():
                qbt_client.torrents_delete(delete_files=False, hashes=i.hash)

    @classmethod
    def delete_all_data(cls) -> None:
        logger.debug(f"Deleting all torrent + files")
        with qbittorrentapi.Client(**BOT_CONFIGS.clients.connection_string) as qbt_client:
            for i in qbt_client.torrents_info():
                qbt_client.torrents_delete(delete_files=True, hashes=i.hash)

    @classmethod
    def get_categories(cls):
        with qbittorrentapi.Client(**BOT_CONFIGS.clients.connection_string) as qbt_client:
            categories = qbt_client.torrent_categories.categories
            if len(categories) > 0:
                return categories

            else:
                return

    @classmethod
    def get_torrent_info(cls, torrent_hash: str = None, status_filter: str = None):
        if torrent_hash is None:
            logger.debug("Getting torrents infos")
            with qbittorrentapi.Client(**BOT_CONFIGS.clients.connection_string) as qbt_client:
                return qbt_client.torrents_info(status_filter=status_filter)
        logger.debug(f"Getting infos for torrent with hash {torrent_hash}")
        with qbittorrentapi.Client(**BOT_CONFIGS.clients.connection_string) as qbt_client:
            return next(
                iter(
                    qbt_client.torrents_info(status_filter=status_filter, torrent_hashes=torrent_hash)
                ), None
            )

    @classmethod
    def edit_category(cls, name: str, save_path: str) -> None:
        logger.debug(f"Editing category {name}, new save path: {save_path}")
        with qbittorrentapi.Client(**BOT_CONFIGS.clients.connection_string) as qbt_client:
            qbt_client.torrents_edit_category(
                name=name,
                save_path=save_path
            )

    @classmethod
    def create_category(cls, name: str, save_path: str) -> None:
        logger.debug(f"Creating new category {name} with save path: {save_path}")
        with qbittorrentapi.Client(**BOT_CONFIGS.clients.connection_string) as qbt_client:
            qbt_client.torrents_create_category(
                name=name,
                save_path=save_path
            )

    @classmethod
    def remove_category(cls, name: str) -> None:
        logger.debug(f"Removing category {name}")
        with qbittorrentapi.Client(**BOT_CONFIGS.clients.connection_string) as qbt_client:
            qbt_client.torrents_remove_categories(categories=name)

    @classmethod
    def check_connection(cls) -> str:
        logger.debug("Checking Qbt Connection")
        with qbittorrentapi.Client(**BOT_CONFIGS.clients.connection_string) as qbt_client:
            return qbt_client.app.version
