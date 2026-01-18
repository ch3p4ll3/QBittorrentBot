from enum import Enum


class ClientTypeEnum(str, Enum):
    QBittorrent = 'qbittorrent'


class UserRolesEnum(str, Enum):
    Reader = "reader"
    Manager = "manager"
    Administrator = "administrator"


class TelegramProxyScheme(str, Enum):
    Sock4 = "socks4"
    Sock5 = "socks5"
    Http = "http"