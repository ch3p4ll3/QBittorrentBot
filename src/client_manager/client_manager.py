from io import BytesIO
from typing import Union, List
from abc import ABC


class ClientManager(ABC):
    @classmethod
    def add_magnet(cls, magnet_link: Union[str, List[str]], category: str = None) -> bool:
        """Add one or multiple magnet links with or without a category, return true if successful"""
        raise NotImplementedError

    @classmethod
    def add_torrent(cls, file_name: str, category: str = None) -> bool:
        """Add one torrent file with or without a category, return true if successful"""
        raise NotImplementedError

    @classmethod
    def resume_all(cls) -> None:
        """Resume all torrents"""
        raise NotImplementedError

    @classmethod
    def pause_all(cls) -> None:
        """Pause all torrents"""
        raise NotImplementedError

    @classmethod
    def resume(cls, torrent_hash: str) -> None:
        """Resume a specific torrent"""
        raise NotImplementedError

    @classmethod
    def pause(cls, torrent_hash: str) -> None:
        """Pause a specific torrent"""
        raise NotImplementedError

    @classmethod
    def delete_one_no_data(cls, torrent_hash: str) -> None:
        """Delete a specific torrent without deleting the data"""
        raise NotImplementedError

    @classmethod
    def delete_one_data(cls, torrent_hash: str) -> None:
        """Delete a specific torrent deleting the data"""
        raise NotImplementedError

    @classmethod
    def delete_all_no_data(cls) -> None:
        """Delete all torrents without deleting the data"""
        raise NotImplementedError

    @classmethod
    def delete_all_data(cls) -> None:
        """Delete all torrents deleting the data"""
        raise NotImplementedError

    @classmethod
    def get_categories(cls):
        """Get categories"""
        raise NotImplementedError

    @classmethod
    def get_torrent_info(cls, torrent_hash: str = None, status_filter: str = None):
        """Get a torrent info with or without a status filter"""
        raise NotImplementedError

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
        raise NotImplementedError

    @classmethod
    def export_torrent(cls, torrent_hash: str) -> BytesIO:
        """Export a .torrent file for the torrent."""
        raise NotImplementedError

    @classmethod
    def get_speed_limit_mode(cls) -> bool:
        """Get speed limit of the client, returns True if speed limit is active"""
        raise NotImplementedError

    @classmethod
    def toggle_speed_limit(cls) -> bool:
        """Toggle speed limit of the client, returns True if speed limit is active"""
        raise NotImplementedError
