from aiogram.filters.callback_data import CallbackData


class TorrentInfo(CallbackData, prefix="torrentInfo"):
    torrent_hash: str


class Export(CallbackData, prefix="export"):
    torrent_hash: str
