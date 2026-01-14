from io import BytesIO
from typing import Union, List
from abc import ABC


from settings import Settings


class ClientManager(ABC):
    def __init__(self, settings: Settings):
        self.settings = settings
    
    def add_magnet(self, magnet_link: Union[str, List[str]], category: str = None) -> bool:
        """Add one or multiple magnet links with or without a category, return true if successful"""
        raise NotImplementedError
    
    def add_torrent(self, file_name: str, category: str = None) -> bool:
        """Add one torrent file with or without a category, return true if successful"""
        raise NotImplementedError
    
    def resume_all(self) -> None:
        """Resume all torrents"""
        raise NotImplementedError

    def pause_all(self) -> None:
        """Pause all torrents"""
        raise NotImplementedError

    def resume(self, torrent_hash: str) -> None:
        """Resume a specific torrent"""
        raise NotImplementedError

    def pause(self, torrent_hash: str) -> None:
        """Pause a specific torrent"""
        raise NotImplementedError
    
    def delete_one_no_data(self, torrent_hash: str) -> None:
        """Delete a specific torrent without deleting the data"""
        raise NotImplementedError
    
    def delete_one_data(self, torrent_hash: str) -> None:
        """Delete a specific torrent deleting the data"""
        raise NotImplementedError
    
    def delete_all_no_data(self) -> None:
        """Delete all torrents without deleting the data"""
        raise NotImplementedError

    def delete_all_data(self) -> None:
        """Delete all torrents deleting the data"""
        raise NotImplementedError

    def get_categories(self):
        """Get categories"""
        raise NotImplementedError
    
    def get_torrent(self, torrent_hash: str, status_filter: str = None):
        """Get a torrent info with or without a status filter"""
        raise NotImplementedError
    
    def get_torrents(self, torrent_hash: str = None, status_filter: str = None):
        """Get a torrent info with or without a status filter"""
        raise NotImplementedError
    
    def edit_category(self, name: str, save_path: str) -> None:
        """Edit a category save path"""
        raise NotImplementedError
    
    def create_category(self, name: str, save_path: str) -> None:
        """Create a new category"""
        raise NotImplementedError
    
    def remove_category(self, name: str) -> None:
        """Delete a category"""
        raise NotImplementedError
    
    def check_connection(self) -> str:
        """Check connection with Client"""
        raise NotImplementedError
    
    def export_torrent(self, torrent_hash: str) -> BytesIO:
        """Export a .torrent file for the torrent."""
        raise NotImplementedError
    
    def get_speed_limit_mode(self) -> bool:
        """Get speed limit of the client, returns True if speed limit is active"""
        raise NotImplementedError
    
    def toggle_speed_limit(self) -> bool:
        """Toggle speed limit of the client, returns True if speed limit is active"""
        raise NotImplementedError
