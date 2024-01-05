from enum import StrEnum


class Strings(StrEnum):
    GenericError = "errors.error"
    PathNotValid = "errors.path_not_valid"
    CommandDoesNotExist = "errors.command_does_not_exist"

    # On Message
    UnableToAddMagnet = "on_message.error_adding_magnet"
    InvalidMagnet = "on_message.invalid_magnet"
    UnableToAddTorrent = "on_message.error_adding_torrent"
    InvalidTorrent = "on_message.invalid_torrent"
    CategoryPath = "on_message.send_category_path"

    # Common
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

    # Commands
    NotAuthorized = "commands.not_authorized"
    StatsCommand = "commands.stats_command"

    ########################## CALLBACKS ###################################
    # Torrent Info
    TorrentCompleted = "callbacks.torrent_info.torrent_completed"
    TorrentState = "callbacks.torrent_info.torrent_state"
    TorrentSize = "callbacks.torrent_info.torrent_size"
    TorrentEta = "callbacks.torrent_info.torrent_eta"
    TorrentCategory = "callbacks.torrent_info.torrent_category"
    
    ExportTorrentBtn = "callbacks.torrent_infoinfo_btns.export_torrent"
    PauseTorrentBtn = "callbacks.torrent_infoinfo_btns.pause_torrent"
    ResumeTorrentBtn = "callbacks.torrent_infoinfo_btns.resume_torrent"
    DeleteTorrentBtn = "callbacks.torrent_infoinfo_btns.delete_torrent"

    # add_torrents
    SendMagnetLink = "callbacks.add_torrents.send_magnet"
    SendTorrentFile = "callbacks.add_torrents.send_torrent"

    # Settings
    SettingsMenu = "callbacks.settings.settings_menu"
    UsersSettings = "callbacks.settings.settings_menu_btns.users_settings"
    ClientSettings = "callbacks.settings.settings_menu_btns.client_settings"
    ReloadSettings = "callbacks.settings.settings_menu_btns.reload_settings"

    # Client Settings
    Enabled = "callbacks.client_settings.enabled"
    Disabled = "callbacks.client_settings.disabled"
    SpeedLimitStatus = "callbacks.client_settings.speed_limit_status"
    EditClientSettings = "callbacks.client_settings.edit_client_settings"

    EditClientSettingsBtn = "callbacks.client_settings.edit_client_settings_btns.edit_client_settings"
    ToggleSpeedLimit = "callbacks.client_settings.edit_client_settings_btns.toggle_speed_limit"
    CheckClientConnection = "callbacks.client_settings.edit_client_settings_btns.check_client_connection"
    BackToSettings = "callbacks.client_settings.edit_client_settings_btns.back_to_settings"

    ClientConnectionOk = "callbacks.client_settings.client_connection_ok"
    ClientConnectionBad = "callbacks.client_settings.client_connection_bad"

    EditClientSetting = "callbacks.client_settings.edit_client_setting"
    EditClientType = "callbacks.client_settings.edit_client_type"

    NewValueForClientField = "callbacks.client_settings.new_value_for_field"