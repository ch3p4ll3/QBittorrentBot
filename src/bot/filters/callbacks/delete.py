from aiogram.filters.callback_data import CallbackData


class DeleteMenu(CallbackData, prefix="menu_delete"):
    pass


class DeleteOne(CallbackData, prefix="delete_one"):
    torrent_hash: str


class DeleteOneNoData(CallbackData, prefix="delete_one_no_data"):
    torrent_hash: str


class DeleteOneData(CallbackData, prefix="delete_one_data"):
    torrent_hash: str


class DeleteAll(CallbackData, prefix="delete_all"):
    pass


class DeleteAllNoData(CallbackData, prefix="delete_all_no_data"):
    pass


class DeleteAllData(CallbackData, prefix="delete_all_data"):
    pass