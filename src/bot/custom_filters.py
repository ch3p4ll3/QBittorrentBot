from pyrogram import filters
from ..configs import Configs
from ..utils import get_user_from_config
from ..configs.enums import UserRolesEnum


# Authorization filters
check_user_filter = filters.create(lambda _, __, message: message.from_user.id in [i.user_id for i in Configs.config.users])

user_is_reader = filters.create(lambda _, __, query: get_user_from_config(query.from_user.id).role == UserRolesEnum.Reader)
user_is_manager = filters.create(lambda _, __, query: get_user_from_config(query.from_user.id).role == UserRolesEnum.Manager)
user_is_administrator = filters.create(lambda _, __, query: get_user_from_config(query.from_user.id).role == UserRolesEnum.Administrator)

# Categories filters
menu_category_filter = filters.create(lambda _, __, query: query.data == "menu_categories")
add_category_filter = filters.create(lambda _, __, query: query.data == "add_category")
remove_category_filter = filters.create(lambda _, __, query: query.data.startswith("remove_category"))
modify_category_filter = filters.create(lambda _, __, query: query.data.startswith("modify_category"))
category_filter = filters.create(lambda _, __, query: query.data.startswith("category"))
select_category_filter = filters.create(lambda _, __, query: query.data.startswith("select_category"))

# Add filters
add_magnet_filter = filters.create(lambda _, __, query: query.data.startswith("add_magnet"))
add_torrent_filter = filters.create(lambda _, __, query: query.data.startswith("add_torrent"))

# Pause/Resume filters
menu_pause_resume_filter = filters.create(lambda _, __, query: query.data == "menu_pause_resume")
pause_all_filter = filters.create(lambda _, __, query: query.data.startswith("pause_all"))
resume_all_filter = filters.create(lambda _, __, query: query.data.startswith("resume_all"))
pause_filter = filters.create(lambda _, __, query: query.data.startswith("pause"))
resume_filter = filters.create(lambda _, __, query: query.data.startswith("resume"))

# Delete filers
menu_delete_filter = filters.create(lambda _, __, query: query.data == "menu_delete")
delete_one_filter = filters.create(lambda _, __, query: query.data.split("#")[0] == "delete_one")
delete_one_no_data_filter = filters.create(lambda _, __, query: query.data.startswith("delete_one_no_data"))
delete_one_data_filter = filters.create(lambda _, __, query: query.data.startswith("delete_one_data"))
delete_all_filter = filters.create(lambda _, __, query: query.data.split("#")[0] == "delete_all")
delete_all_no_data_filter = filters.create(lambda _, __, query: query.data.startswith("delete_all_no_data"))
delete_all_data_filter = filters.create(lambda _, __, query: query.data.startswith("delete_all_data"))

# Settings filters
settings_filter = filters.create(lambda _, __, query: query.data == "settings")
get_users_filter = filters.create(lambda _, __, query: query.data == "get_users")
user_info_filter = filters.create(lambda _, __, query: query.data.startswith("user_info"))
edit_user_filter = filters.create(lambda _, __, query: query.data.startswith("edit_user"))
toggle_user_var_filter = filters.create(lambda _, __, query: query.data.startswith("toggle_user_var"))
edit_client_settings_filter = filters.create(lambda _, __, query: query.data == "edit_client")
list_client_settings_filter = filters.create(lambda _, __, query: query.data == "lst_client")
check_connection_filter = filters.create(lambda _, __, query: query.data == "check_connection")
edit_client_setting_filter = filters.create(lambda _, __, query: query.data.startswith("edit_clt"))
reload_settings_filter = filters.create(lambda _, __, query: query.data == "reload_settings")


# Other
torrentInfo_filter = filters.create(lambda _, __, query: query.data.startswith("torrentInfo"))
menu_filter = filters.create(lambda _, __, query: query.data == "menu")
list_filter = filters.create(lambda _, __, query: query.data.startswith("list"))
list_by_status_filter = filters.create(lambda _, __, query: query.data.split("#")[0] == "by_status_list")
