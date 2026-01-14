from aiogram.filters.callback_data import CallbackData


class TorrentInfo(CallbackData, prefix="torrentInfo"):
    torrent_hash: str


class Export(CallbackData, prefix="export"):
    torrent_hash: str


class Pause(CallbackData, prefix="pause"):
    torrent_hash: str


class Resume(CallbackData, prefix="resume"):
    torrent_hash: str


class DeleteOne(CallbackData, prefix="delete_one"):
    torrent_hash: str
