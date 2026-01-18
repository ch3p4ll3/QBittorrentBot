from aiogram.filters.callback_data import CallbackData


class AddMagnet(CallbackData, prefix="add_magnet"):
    category: str | None


class AddTorrent(CallbackData, prefix="add_torrent"):
    category: str | None
