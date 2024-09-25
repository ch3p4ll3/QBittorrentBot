from typing import List, Union

from ..entities.torrent import Torrent
from .mapper import Mapper
from transmission_rpc.torrent import Torrent as TransmissionTorrent


class TransmissionMapper(Mapper):
    @classmethod
    def map(cls, torrents: Union[TransmissionTorrent, List[TransmissionTorrent]]) -> Union[Torrent, List[Torrent]]:
        if isinstance(torrents, List[TransmissionTorrent]):
            return [
                Torrent(
                    torrent.info_hash,
                    torrent.name,
                    torrent.progress,
                    torrent.rate_download,
                    torrent.status,
                    torrent.total_size,
                    torrent.eta,
                    None
                )
                for torrent in torrents
            ]

        return Torrent(
            torrents.info_hash,
            torrents.name,
            torrents.progress,
            torrents.rate_download,
            torrents.status,
            torrents.total_size,
            torrents.eta,
            None
        )
