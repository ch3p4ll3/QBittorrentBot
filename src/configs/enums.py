from enum import Enum


class ClientTypeEnum(str, Enum):
    QBittorrent = 'qbittorrent'
    Transmission = 'transmission'


class UserRolesEnum(str, Enum):
    Reader = "reader"
    Manager = "manager"
    Administrator = "administrator"


class TorrentStatusEnum(Enum):
    Downloading = {
        ClientTypeEnum.QBittorrent: 'downloading',
        ClientTypeEnum.Transmission: 'downloading'
    }
    Completed = {
        ClientTypeEnum.QBittorrent: 'completed',
        ClientTypeEnum.Transmission: 'seeding'
    }
    Paused = {
        ClientTypeEnum.QBittorrent: 'paused',
        ClientTypeEnum.Transmission: 'stopped'
    }
    Stalled = {
        ClientTypeEnum.QBittorrent: 'stalled',
        ClientTypeEnum.Transmission: 'download pending'
    }


class TelegramProxyScheme(str, Enum):
    Sock4 = "socks4"
    Sock5 = "socks5"
    Http = "http"