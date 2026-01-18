from io import BytesIO
from typing import Union, List
import logging

import qbittorrentapi

from src.settings import Settings
from ..client_manager import ClientManager
from .async_qbittorrent_client import AsyncQbittorrentClient

from ..mappers.mapper_repo import MapperRepo
from ..entities.torrent import Torrent

logger = logging.getLogger(__name__)


class QbittorrentManager(ClientManager):
    def __init__(self, settings: Settings):
        self.settings = settings
        super().__init__(settings)
    
    def _client(self) -> AsyncQbittorrentClient:
        return AsyncQbittorrentClient(**self.settings.client.connection_string)

    async def add_magnet(self, magnet_link: Union[str, List[str]], category: str = None) -> bool:
        if category == "None":
            category = None

        async with self._client() as qbt:
            logger.debug(f"Adding magnet with category {category}")
            result = await qbt.call(qbt.client.torrents_add, urls=magnet_link, category=category)

        return result == "Ok."

    async def add_torrent(self, file_name: str, category: str = None) -> bool:
        if category == "None":
            category = None

        try:
            async with self._client() as qbt:
                logger.debug(f"Adding torrent with category {category}")
                result = await qbt.call(qbt.client.torrents_add, torrent_files=file_name, category=category)
            return result == "Ok."

        except qbittorrentapi.exceptions.UnsupportedMediaType415Error:
            pass

    async def resume_all(self) -> None:
        logger.debug("Resuming all torrents")
        async with self._client() as qbt:
            await qbt.call(qbt.client.torrents.resume.all)

    async def pause_all(self) -> None:
        logger.debug("Pausing all torrents")
        async with self._client() as qbt:
            await qbt.call(qbt.client.torrents.pause.all)

    async def resume(self, torrent_hash: str) -> None:
        logger.debug(f"Resuming torrent with has {torrent_hash}")
        async with self._client() as qbt:
            await qbt.call(qbt.client.torrents_resume, torrent_hashes=torrent_hash)

    async def pause(self, torrent_hash: str) -> None:
        logger.debug(f"Pausing torrent with hash {torrent_hash}")
        async with self._client() as qbt:
            await qbt.call(qbt.client.torrents_pause, torrent_hashes=torrent_hash)

    async def delete_one_no_data(self, torrent_hash: str) -> None:
        logger.debug(f"Deleting torrent with hash {torrent_hash} without removing files")
        async with self._client() as qbt:
            await qbt.call(qbt.client.torrents_delete, delete_files=False, torrent_hashes=torrent_hash)

    async def delete_one_data(self, torrent_hash: str) -> None:
        logger.debug(f"Deleting torrent with hash {torrent_hash} + removing files")
        async with self._client() as qbt:
            await qbt.call(qbt.client.torrents_delete, delete_files=True, torrent_hashes=torrent_hash)

    async def delete_all_no_data(self) -> None:
        logger.debug("Deleting all torrents")
        async with self._client() as qbt:
            for i in await qbt.call(qbt.client.torrents_info()):
                await qbt.call(qbt.client.torrents_delete, delete_files=False, hashes=i.hash)

    async def delete_all_data(self) -> None:
        logger.debug("Deleting all torrent + files")
        async with self._client() as qbt:
            for i in await qbt.call(qbt.client.torrents_info()):
                await qbt.call(qbt.client.torrents_delete, delete_files=True, hashes=i.hash)

    async def get_categories(self):
        async with self._client() as qbt:
            categories = qbt.client.torrent_categories.categories
            if len(categories) > 0:
                return categories

            else:
                return

    async def get_torrent(self, torrent_hash: str, status_filter: str = None) -> Union[Torrent, None]:
        logger.debug(f"Getting torrent with hash {torrent_hash}")
        async with self._client() as qbt:
            mapper = MapperRepo.get_mapper(self.settings.client.type)

            torrent = next(
                iter(
                    await qbt.call(qbt.client.torrents_info, status_filter=status_filter, torrent_hashes=torrent_hash)
                ), None
            )
            return mapper.map(torrent)

    async def get_torrents(self, torrent_hash: str = None, status_filter: str = None) -> List[Torrent]:
        if torrent_hash is None:
            logger.debug("Getting torrents infos")
            async with self._client() as qbt:
                mapper = MapperRepo.get_mapper(self.settings.client.type)
                torrents = await qbt.call(qbt.client.torrents_info, status_filter=status_filter)
                return mapper.map(torrents)

    async def edit_category(self, name: str, save_path: str) -> None:
        logger.debug(f"Editing category {name}, new save path: {save_path}")
        async with self._client() as qbt:
            await qbt.call(qbt.client.torrents_edit_category, name=name, save_path=save_path)

    async def create_category(self, name: str, save_path: str) -> None:
        logger.debug(f"Creating new category {name} with save path: {save_path}")
        async with self._client() as qbt:
            await qbt.call(qbt.client.torrents_create_category, name=name, save_path=save_path)

    async def remove_category(self, name: str) -> None:
        logger.debug(f"Removing category {name}")
        async with self._client() as qbt:
            await qbt.call(qbt.client.torrents_remove_categories, categories=name)

    async def check_connection(self) -> str:
        logger.debug("Checking Qbt Connection")
        async with self._client() as qbt:
            return qbt.client.app.version

    async def export_torrent(self, torrent_hash: str) -> BytesIO:
        logger.debug(f"Exporting torrent with hash {torrent_hash}")
        async with self._client() as qbt:
            torrent_bytes = await qbt.call(qbt.client.torrents_export, torrent_hash=torrent_hash)
            torrent_name = await qbt.call(qbt.client.torrents_info, torrent_hashes=torrent_hash)
            torrent_name = torrent_name[0].name

            file_to_return = BytesIO(torrent_bytes)
            file_to_return.name = f"{torrent_name}.torrent"
            return file_to_return

    async def get_speed_limit_mode(self) -> bool:
        async with self._client() as qbt:
            return qbt.client.transfer.speedLimitsMode == "1"

    async def toggle_speed_limit(self) -> bool:
        async with self._client() as qbt:
            await qbt.call(qbt.client.transfer.setSpeedLimitsMode)
            return qbt.client.transfer.speedLimitsMode == "1"
