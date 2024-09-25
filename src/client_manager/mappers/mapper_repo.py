from ...configs.enums import ClientTypeEnum
from .qbittorrent_mapper import QBittorrentMapper
from .mapper import Mapper
from .transmission_mapper import TransmissionMapper


class MapperRepo:
    mappers = {
        ClientTypeEnum.QBittorrent: QBittorrentMapper,
        ClientTypeEnum.Transmission: TransmissionMapper
    }

    @classmethod
    def get_mapper(cls, client_type: ClientTypeEnum):
        return cls.mappers.get(client_type, Mapper)
