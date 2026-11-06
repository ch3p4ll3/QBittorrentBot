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


def _added_ok(result) -> bool:
    # qBittorrent < 5.1 answers "Ok."/"Fails."; >= 5.1 answers JSON
    # (TorrentsAddedMetadata) with success/pending/failure counts.
    if isinstance(result, str):
        return result == "Ok."
    try:
        return (result.get("success_count", 0) + result.get("pending_count", 0)) > 0
    except AttributeError:
        return False


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

        return _added_ok(result)

    async def add_torrent(self, file_name: str, category: str = None) -> bool:
        if category == "None":
            category = None

        try:
            async with self._client() as qbt:
                logger.debug(f"Adding torrent with category {category}")
                result = await qbt.call(qbt.client.torrents_add, torrent_files=file_name, category=category)
            return _added_ok(result)

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

    async def set_torrents_category(self, category: str, torrent_hashes: str | List[str]):
        async with self._client() as qbt:
            await qbt.call(qbt.client.torrents_set_category, category=category, torrent_hashes=torrent_hashes)

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

    @staticmethod
    def _flatten_feeds(items: dict, prefix: str = "") -> dict:
        """RSS items are a tree of folders and feeds; feeds carry a 'url'. Returns {path: url}."""
        feeds = {}
        for name, value in (items or {}).items():
            path = f"{prefix}{name}"
            if isinstance(value, dict) and "url" in value:
                feeds[path] = value["url"]
            elif isinstance(value, dict):
                feeds.update(QbittorrentManager._flatten_feeds(value, prefix=f"{path}\\"))
        return feeds

    async def rss_get_feeds(self) -> dict:
        async with self._client() as qbt:
            items = await qbt.call(qbt.client.rss_items, include_feed_data=False)
        return self._flatten_feeds(items)

    async def rss_add_feed(self, name: str, url: str) -> None:
        logger.debug(f"Adding RSS feed {name}")
        async with self._client() as qbt:
            await qbt.call(qbt.client.rss_add_feed, url=url, item_path=name)

    async def rss_remove_feed(self, name: str) -> None:
        logger.debug(f"Removing RSS feed {name}")
        async with self._client() as qbt:
            await qbt.call(qbt.client.rss_remove_item, item_path=name)

    async def rss_mark_all_read(self, name: str) -> None:
        async with self._client() as qbt:
            await qbt.call(qbt.client.rss_mark_as_read, item_path=name)

    async def rss_get_rules(self) -> dict:
        async with self._client() as qbt:
            return dict(await qbt.call(qbt.client.rss_rules))

    async def rss_set_rule(self, name: str, rule_def: dict) -> None:
        logger.debug(f"Setting RSS rule {name}")
        async with self._client() as qbt:
            await qbt.call(qbt.client.rss_set_rule, rule_name=name, rule_def=rule_def)

    async def rss_remove_rule(self, name: str) -> None:
        logger.debug(f"Removing RSS rule {name}")
        async with self._client() as qbt:
            await qbt.call(qbt.client.rss_remove_rule, rule_name=name)
