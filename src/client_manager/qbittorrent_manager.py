from io import BytesIO

import qbittorrentapi
import logging
from src.configs import Configs
from typing import Union, List
from .client_manager import ClientManager

from .mappers.mapper_repo import MapperRepo
from .entities.torrent import Torrent

logger = logging.getLogger(__name__)


class QbittorrentManager(ClientManager):
    @classmethod
    def add_magnet(cls, magnet_link: Union[str, List[str]], category: str = None) -> bool:
        if category == "None":
            category = None

        with qbittorrentapi.Client(**Configs.config.client.connection_string) as qbt_client:
            logger.debug(f"Adding magnet with category {category}")
            result = qbt_client.torrents_add(urls=magnet_link, category=category)

        return result == "Ok."

    @classmethod
    def add_torrent(cls, file_name: str, category: str = None) -> bool:
        if category == "None":
            category = None

        try:
            with qbittorrentapi.Client(**Configs.config.client.connection_string) as qbt_client:
                logger.debug(f"Adding torrent with category {category}")
                result = qbt_client.torrents_add(torrent_files=file_name, category=category)
            return result == "Ok."

        except qbittorrentapi.exceptions.UnsupportedMediaType415Error:
            pass

    @classmethod
    def resume_all(cls) -> None:
        logger.debug("Resuming all torrents")
        with qbittorrentapi.Client(**Configs.config.client.connection_string) as qbt_client:
            qbt_client.torrents.resume.all()

    @classmethod
    def pause_all(cls) -> None:
        logger.debug("Pausing all torrents")
        with qbittorrentapi.Client(**Configs.config.client.connection_string) as qbt_client:
            qbt_client.torrents.pause.all()

    @classmethod
    def resume(cls, torrent_hash: str) -> None:
        logger.debug(f"Resuming torrent with has {torrent_hash}")
        with qbittorrentapi.Client(**Configs.config.client.connection_string) as qbt_client:
            qbt_client.torrents_resume(torrent_hashes=torrent_hash)

    @classmethod
    def pause(cls, torrent_hash: str) -> None:
        logger.debug(f"Pausing torrent with hash {torrent_hash}")
        with qbittorrentapi.Client(**Configs.config.client.connection_string) as qbt_client:
            qbt_client.torrents_pause(torrent_hashes=torrent_hash)

    @classmethod
    def delete_one_no_data(cls, torrent_hash: str) -> None:
        logger.debug(f"Deleting torrent with hash {torrent_hash} without removing files")
        with qbittorrentapi.Client(**Configs.config.client.connection_string) as qbt_client:
            qbt_client.torrents_delete(
                delete_files=False,
                torrent_hashes=torrent_hash
            )

    @classmethod
    def delete_one_data(cls, torrent_hash: str) -> None:
        logger.debug(f"Deleting torrent with hash {torrent_hash} + removing files")
        with qbittorrentapi.Client(**Configs.config.client.connection_string) as qbt_client:
            qbt_client.torrents_delete(
                delete_files=True,
                torrent_hashes=torrent_hash
            )

    @classmethod
    def delete_all_no_data(cls) -> None:
        logger.debug("Deleting all torrents")
        with qbittorrentapi.Client(**Configs.config.client.connection_string) as qbt_client:
            for i in qbt_client.torrents_info():
                qbt_client.torrents_delete(delete_files=False, hashes=i.hash)

    @classmethod
    def delete_all_data(cls) -> None:
        logger.debug("Deleting all torrent + files")
        with qbittorrentapi.Client(**Configs.config.client.connection_string) as qbt_client:
            for i in qbt_client.torrents_info():
                qbt_client.torrents_delete(delete_files=True, hashes=i.hash)

    @classmethod
    def get_categories(cls):
        with qbittorrentapi.Client(**Configs.config.client.connection_string) as qbt_client:
            categories = qbt_client.torrent_categories.categories
            if len(categories) > 0:
                return categories

            else:
                return

    @classmethod
    def get_torrent(cls, torrent_hash: str, status_filter: str = None) -> Union[Torrent, None]:
        logger.debug(f"Getting torrent with hash {torrent_hash}")
        with qbittorrentapi.Client(**Configs.config.client.connection_string) as qbt_client:
            mapper = MapperRepo.get_mapper(Configs.config.client.type)

            torrent = next(
                iter(
                    qbt_client.torrents_info(status_filter=status_filter, torrent_hashes=torrent_hash)
                ), None
            )
            return mapper.map(torrent)

    @classmethod
    def get_torrents(cls, status_filter: str = None) -> List[Torrent]:
        logger.debug("Getting torrents infos")
        with qbittorrentapi.Client(**Configs.config.client.connection_string) as qbt_client:
            mapper = MapperRepo.get_mapper(Configs.config.client.type)
            return mapper.map(qbt_client.torrents_info(status_filter=status_filter))

    @classmethod
    def edit_category(cls, name: str, save_path: str) -> None:
        logger.debug(f"Editing category {name}, new save path: {save_path}")
        with qbittorrentapi.Client(**Configs.config.client.connection_string) as qbt_client:
            qbt_client.torrents_edit_category(
                name=name,
                save_path=save_path
            )

    @classmethod
    def create_category(cls, name: str, save_path: str) -> None:
        logger.debug(f"Creating new category {name} with save path: {save_path}")
        with qbittorrentapi.Client(**Configs.config.client.connection_string) as qbt_client:
            qbt_client.torrents_create_category(
                name=name,
                save_path=save_path
            )

    @classmethod
    def remove_category(cls, name: str) -> None:
        logger.debug(f"Removing category {name}")
        with qbittorrentapi.Client(**Configs.config.client.connection_string) as qbt_client:
            qbt_client.torrents_remove_categories(categories=name)

    @classmethod
    def check_connection(cls) -> str:
        logger.debug("Checking Qbt Connection")
        with qbittorrentapi.Client(**Configs.config.client.connection_string) as qbt_client:
            return qbt_client.app.version

    @classmethod
    def export_torrent(cls, torrent_hash: str) -> BytesIO:
        logger.debug(f"Exporting torrent with hash {torrent_hash}")
        with qbittorrentapi.Client(**Configs.config.client.connection_string) as qbt_client:
            torrent_bytes = qbt_client.torrents_export(torrent_hash=torrent_hash)
            torrent_name = qbt_client.torrents_info(torrent_hashes=torrent_hash)[0].name

            file_to_return = BytesIO(torrent_bytes)
            file_to_return.name = f"{torrent_name}.torrent"
            return file_to_return

    @classmethod
    def get_speed_limit_mode(cls) -> bool:
        with qbittorrentapi.Client(**Configs.config.client.connection_string) as qbt_client:
            return qbt_client.transfer.speedLimitsMode == "1"

    @classmethod
    def toggle_speed_limit(cls) -> bool:
        with qbittorrentapi.Client(**Configs.config.client.connection_string) as qbt_client:
            qbt_client.transfer.setSpeedLimitsMode()
            return qbt_client.transfer.speedLimitsMode == "1"
