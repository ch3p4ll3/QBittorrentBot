from abc import ABC
from typing import Union, List, Any
from ..entities.torrent import Torrent


class Mapper(ABC):
    @classmethod
    def map(cls, torrents: Union[Any, List[Any]]) -> Union[Torrent, List[Torrent]]:
        """Map a torrent or list of torrents to a mapped torrent or list of torrents"""
        raise NotImplementedError
