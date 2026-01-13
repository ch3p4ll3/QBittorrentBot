from settings.enums import ClientTypeEnum
from .qbittorrent_manager import QbittorrentManager, ClientManager


class ClientRepo:
    repositories = {
        ClientTypeEnum.QBittorrent: QbittorrentManager
    }

    @classmethod
    def get_client_manager(cls, client_type: ClientTypeEnum):
        return cls.repositories.get(client_type, ClientManager)
