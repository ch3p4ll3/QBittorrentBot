from ...configs.enums import ClientTypeEnum
from .qbittorrent_mapper import QBittorrentMapper, Mapper


class MapperRepo:
    mappers = {
        ClientTypeEnum.QBittorrent: QBittorrentMapper
    }

    @classmethod
    def get_mapper(cls, client_type: ClientTypeEnum):
        return cls.mappers.get(client_type, Mapper)
