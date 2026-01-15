from aiogram.filters.callback_data import CallbackData

from .category import AddCategory, SelectCategory, CategoryMenu, RemoveCategory, ModifyCategory, CategoryAction
from .add_torrents import AddMagnet, AddTorrent
from .list import List, ListByStatus, Menu
from .torrent_info import TorrentInfo, Export, Pause, Resume, DeleteOne
from .pause_resume import PauseResumeMenu, Pause, PauseAll, Resume, ResumeAll


class Menu(CallbackData, prefix="menu"):
    pass
