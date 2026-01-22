from aiogram.filters.callback_data import CallbackData

from .category import AddCategory, SelectCategory, CategoryMenu, RemoveCategory, ModifyCategory, CategoryAction
from .add_torrents import AddMagnet, AddTorrent
from .list import List, ListByStatus, Menu
from .torrent_info import TorrentInfo, Export
from .pause_resume import PauseResumeMenu, Pause, PauseAll, Resume, ResumeAll
from .delete import DeleteAll, DeleteAllData, DeleteAllNoData, DeleteMenu, DeleteOne, DeleteOneData, DeleteOneNoData
from .settings import SettingsMenu, EditClientMenu, ReloadSettingsMenu, ToggleSpeedLimit, CheckConnection
