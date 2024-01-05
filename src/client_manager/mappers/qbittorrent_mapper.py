from typing import List, Union

from ..entities.torrent import Torrent
from .mapper import Mapper
from qbittorrentapi.torrents import TorrentInfoList, TorrentDictionary


class QBittorrentMapper(Mapper):
    @classmethod
    def map(cls, torrents: Union[TorrentDictionary, TorrentInfoList]) -> Union[Torrent, List[Torrent]]:
        if type(torrents) is TorrentInfoList:
            return [
                Torrent(
                    torrent.info.hash,
                    torrent.name,
                    torrent.progress,
                    torrent.dlspeed,
                    torrent.state,
                    torrent.size,
                    torrent.eta,
                    torrent.category
                )
                for torrent in torrents
            ]

        return Torrent(
            torrents.info.hash,
            torrents.name,
            torrents.progress,
            torrents.dlspeed,
            torrents.state,
            torrents.size,
            torrents.eta,
            torrents.category
        )
