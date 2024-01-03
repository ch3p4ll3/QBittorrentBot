from enum import StrEnum


class Strings(StrEnum):
    GenericError = "errors.error"
    PathNotValid = "errors.path_not_valid"
    CommandDoesNotExist = "errors.command_does_not_exist"

    UnableToAddMagnet = "on_message.error_adding_magnet"
    InvalidMagnet = "on_message.invalid_magnet"
    UnableToAddTorrent = "on_message.error_adding_torrent"
    InvalidTorrent = "on_message.invalid_torrent"
    CategoryPath = "on_message.send_category_path"

    MenuList = "common.menu_btn.menu_list"
    AddMagnet = "common.menu_btn.add_magnet"
    AddTorrent = "common.menu_btn.add_torrent"
    PauseResume = "common.menu_btn.pause_resume"
    Delete = "common.menu_btn.delete"
    Categories = "common.menu_btn.categories"
    Settings = "common.menu_btn.settings"

    Menu = "common.menu"

    ListFilterDownloading = "common.list_filter.downloading"
    ListFilterCompleted = "common.list_filter.completed"
    ListFilterPaused = "common.list_filter.paused"

    NoTorrents = "common.no_torrents"
    BackToMenu = "common.back_to_menu_btn"
