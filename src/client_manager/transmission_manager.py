import logging
from io import BytesIO
from typing import Union, List
from .client_manager import ClientManager

from transmission_rpc import Client
from src.configs import Configs

from .mappers.mapper_repo import MapperRepo
from .entities.torrent import Torrent

logger = logging.getLogger(__name__)


class TransmissionManager(ClientManager):
    @classmethod
    def add_magnet(cls, magnet_link: Union[str, List[str]], category: str = None) -> bool:
        """Add one or multiple magnet links with or without a category, return true if successful"""


        client = Client(**Configs.config.client.connection_string)

        for magnet in magnet_link:
            client.add_torrent(magnet, labels=[category] if category is not None else None)

    @classmethod
    def add_torrent(cls, file_name: str, category: str = None) -> bool:
        """Add one torrent file with or without a category, return true if successful"""
        client = Client(**Configs.config.client.connection_string)

        client.add_torrent(file_name, labels=[category] if category is not None else None)

    @classmethod
    def resume_all(cls) -> None:
        """Resume all torrents"""
        client = Client(**Configs.config.client.connection_string)

        client.start_all()

    @classmethod
    def pause_all(cls) -> None:
        """Pause all torrents"""
        client = Client(**Configs.config.client.connection_string)

        for torrent in client.get_torrents():
            client.stop_torrent(torrent.id)

    @classmethod
    def resume(cls, torrent_hash: str) -> None:
        """Resume a specific torrent"""
        client = Client(**Configs.config.client.connection_string)

        client.start_torrent(torrent_hash)

    @classmethod
    def pause(cls, torrent_hash: str) -> None:
        """Pause a specific torrent"""
        client = Client(**Configs.config.client.connection_string)

        client.stop_torrent(torrent_hash)

    @classmethod
    def delete_one_no_data(cls, torrent_hash: str) -> None:
        """Delete a specific torrent without deleting the data"""
        client = Client(**Configs.config.client.connection_string)

        client.remove_torrent(torrent_hash, delete_data=False)

    @classmethod
    def delete_one_data(cls, torrent_hash: str) -> None:
        """Delete a specific torrent deleting the data"""
        client = Client(**Configs.config.client.connection_string)

        client.remove_torrent(torrent_hash, delete_data=True)

    @classmethod
    def delete_all_no_data(cls) -> None:
        """Delete all torrents without deleting the data"""
        client = Client(**Configs.config.client.connection_string)

        for torrent in client.get_torrents():
            client.remove_torrent(torrent.id, delete_data=False)

    @classmethod
    def delete_all_data(cls) -> None:
        """Delete all torrents deleting the data"""
        client = Client(**Configs.config.client.connection_string)

        for torrent in client.get_torrents():
            client.remove_torrent(torrent.id, delete_data=True)

    @classmethod
    def get_categories(cls):
        """Get categories"""
        raise NotImplementedError

    @classmethod
    def get_torrent(cls, torrent_hash: str, status_filter: str = None):
        """Get a torrent info with or without a status filter"""
        client = Client(**Configs.config.client.connection_string)
        mapper = MapperRepo.get_mapper(Configs.config.client.type)

        torrent = client.get_torrent(torrent_hash)

        return mapper.map(torrent)

    @classmethod
    def get_torrents(cls, status_filter: str = None):
        """Get a torrent info with or without a status filter"""
        logger.debug("Getting torrents infos")
        client = Client(**Configs.config.client.connection_string)
        mapper = MapperRepo.get_mapper(Configs.config.client.type)

        if status_filter:
            torrents = [i for i in client.get_torrents() if i.status.value == status_filter]
        else:
            torrents = client.get_torrents()

        return mapper.map(torrents)

    @classmethod
    def edit_category(cls, name: str, save_path: str) -> None:
        """Edit a category save path"""
        raise NotImplementedError

    @classmethod
    def create_category(cls, name: str, save_path: str) -> None:
        """Create a new category"""
        raise NotImplementedError

    @classmethod
    def remove_category(cls, name: str) -> None:
        """Delete a category"""
        raise NotImplementedError

    @classmethod
    def check_connection(cls) -> str:
        """Check connection with Client"""
        client = Client(**Configs.config.client.connection_string)

        return client.get_session().version

    @classmethod
    def export_torrent(cls, torrent_hash: str) -> BytesIO:
        """Export a .torrent file for the torrent."""
        client = Client(**Configs.config.client.connection_string)

        torrent = client.get_torrent(torrent_hash)

        with open(torrent.torrent_file, "rb") as fh:
            bytesio = BytesIO(fh.read())
            bytesio.name = torrent.name

        return bytesio

    @classmethod
    def get_speed_limit_mode(cls) -> bool:
        """Get speed limit of the client, returns True if speed limit is active"""
        client = Client(**Configs.config.client.connection_string)

        return client.get_session().speed_limit_down_enabled

    @classmethod
    def toggle_speed_limit(cls) -> bool:
        """Toggle speed limit of the client, returns True if speed limit is active"""
        client = Client(**Configs.config.client.connection_string)

        current_session = client.get_session()

        client.set_session(speed_limit_down_enabled=not current_session.speed_limit_down_enabled)

        return not current_session.speed_limit_down_enabled
