from typing import List, Union

from ..entities.torrent import Torrent
from .mapper import Mapper
from transmission_rpc.torrent import Torrent as TransmissionTorrent


class TransmissionMapper(Mapper):
    @classmethod
    def map(cls, torrents: Union[TransmissionTorrent, List[TransmissionTorrent]]) -> Union[Torrent, List[Torrent]]:
        if isinstance(torrents, list):
            return [
                Torrent(
                    torrent.info_hash,
                    torrent.name,
                    torrent.progress / 100,
                    torrent.rate_download,
                    torrent.status,
                    torrent.total_size,
                    0 if torrent.eta is None else torrent.eta.total_seconds(),
                    None
                )
                for torrent in torrents
            ]

        return Torrent(
            torrents.info_hash,
            torrents.name,
            torrents.progress / 100,
            torrents.rate_download,
            torrents.status,
            torrents.total_size,
            0 if torrents.eta is None else torrents.eta.total_seconds(),
            None
        )
