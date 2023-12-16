from enum import Enum


class ClientTypeEnum(str, Enum):
    QBittorrent = 'qbittorrent'


class UserRolesEnum(str, Enum):
    Reader = "reader"
    Manager = "manager"
    Administrator = "administrator"
