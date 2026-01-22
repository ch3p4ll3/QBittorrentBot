from .category import AddCategory, SelectCategory, CategoryMenu, RemoveCategory, ModifyCategory, CategoryAction         # noqa: F401
from .add_torrents import AddMagnet, AddTorrent                                                                         # noqa: F401
from .list import List, ListByStatus, Menu                                                                              # noqa: F401
from .torrent_info import TorrentInfo, Export                                                                           # noqa: F401
from .pause_resume import PauseResumeMenu, Pause, PauseAll, Resume, ResumeAll                                           # noqa: F401
from .delete import DeleteAll, DeleteAllData, DeleteAllNoData, DeleteMenu, DeleteOne, DeleteOneData, DeleteOneNoData    # noqa: F401
from .settings import SettingsMenu, EditClientMenu, ReloadSettingsMenu, ToggleSpeedLimit, CheckConnection               # noqa: F401
