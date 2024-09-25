from ..configs.enums import ClientTypeEnum

from .client_manager import ClientManager
from .qbittorrent_manager import QbittorrentManager
from .transmission_manager import TransmissionManager


class ClientRepo:
    repositories = {
        ClientTypeEnum.QBittorrent: QbittorrentManager,
        ClientTypeEnum.Transmission: TransmissionManager
    }

    @classmethod
    def get_client_manager(cls, client_type: ClientTypeEnum):
        return cls.repositories.get(client_type, ClientManager)
