from .add_torrents_callbacks import get_router as get_add_torrents_router   # noqa: F401
from .list_callbacks import get_router as get_list_router                   # noqa: F401
from .torrent_info import get_router as get_torrent_info_router             # noqa: F401

from .category import get_category_router                                   # noqa: F401
from .pause_resume import get_pause_router, get_resume_router               # noqa: F401
from .delete import get_delete_all_router, get_delete_one_router            # noqa: F401
from .settings import get_settings_router                                   # noqa: F401
