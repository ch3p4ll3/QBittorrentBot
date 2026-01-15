from .add_torrents_callbacks import get_router as get_add_torrents_router
from .list_callbacks import get_router as get_list_router
from .torrent_info import get_router as get_torrent_info_router

from .category import get_category_router
from .pause_resume import get_pause_router, get_resume_router
from .delete import get_delete_all_router, get_delete_one_router