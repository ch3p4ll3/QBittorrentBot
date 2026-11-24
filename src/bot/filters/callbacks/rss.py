from aiogram.filters.callback_data import CallbackData


class RssMenu(CallbackData, prefix="rss_menu"):
    pass


class RssList(CallbackData, prefix="rss_list"):
    kind: str  # "feeds" | "rules"


class RssItem(CallbackData, prefix="rss_item"):
    kind: str  # "feed" | "rule"
    id: str    # short hash of the item name (callback data is limited to 64 bytes)


class RssToggle(CallbackData, prefix="rss_toggle"):
    id: str


class RssDelete(CallbackData, prefix="rss_del"):
    kind: str
    id: str
    confirm: int = 0


class RssAddFeed(CallbackData, prefix="rss_addfeed"):
    watch: int = 0  # 1 when the feed is being added as the first step of "Watch for a name"


class RssWatch(CallbackData, prefix="rss_watch"):
    pass


class RssWatchFeed(CallbackData, prefix="rss_wfeed"):
    id: str


class RssWatchCat(CallbackData, prefix="rss_wcat"):
    id: str  # short hash of the category name, or "-" for none


class RssWatchShow(CallbackData, prefix="rss_wshow"):
    on: int  # 1 when the user says the watched name is a TV show (smart filter + show folder)
