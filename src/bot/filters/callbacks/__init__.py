from aiogram.filters.callback_data import CallbackData
from .category import AddCategory, SelectCategory, CategoryMenu, RemoveCategory, ModifyCategory, CategoryAction
from .add_torrents import AddMagnet, AddTorrent


class Menu(CallbackData, prefix="menu"):
    pass
