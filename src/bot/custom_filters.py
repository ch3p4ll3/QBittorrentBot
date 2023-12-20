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
menu_category_filter = filters.regex(r"^menu_categories$")
add_category_filter = filters.regex(r"^add_category$")
remove_category_filter = filters.regex(r'^remove_category(#.+|$)?$')
modify_category_filter = filters.regex(r'^modify_category(#.+|$)?$')
category_filter = filters.regex(r'^category(#.+|$)?$')
select_category_filter = filters.regex(r'^select_category(#.+|$)?$')

# Add filters
add_magnet_filter = filters.regex(r'^add_magnet(#.+|$)?$')
add_torrent_filter = filters.regex(r'^add_torrent(#.+|$)?$')

# Pause/Resume filters
menu_pause_resume_filter = filters.regex(r"^menu_pause_resume$")
pause_all_filter = filters.regex(r"^pause_all$")
resume_all_filter = filters.regex(r"^resume_all$")
pause_filter = filters.regex(r'^pause(#.+|$)?$')
resume_filter = filters.regex(r'^resume(#.+|$)?$')

# Delete filers
menu_delete_filter = filters.regex(r"^menu_delete$")
delete_one_filter = filters.regex(r'^delete_one(#.+|$)?$')
delete_one_no_data_filter = filters.regex(r'^delete_one_no_data(#.+|$)?$')
delete_one_data_filter = filters.regex(r'^delete_one_data(#.+|$)?$')
delete_all_filter = filters.regex(r'^delete_all(#.+|$)?$')
delete_all_no_data_filter = filters.regex(r"^delete_all_no_data$")
delete_all_data_filter = filters.regex(r"^delete_all_data$")

# Settings filters
settings_filter = filters.regex(r"^settings$")
get_users_filter = filters.regex(r"^get_users$")
user_info_filter = filters.regex(r'^user_info(#.+|$)?$')
edit_user_filter = filters.regex(r'^edit_user(#.+|$)?$')
toggle_user_var_filter = filters.regex(r'^toggle_user_var(#.+|$)?$')
edit_client_settings_filter = filters.regex(r"^edit_client$")
list_client_settings_filter = filters.regex(r"^lst_client$")
check_connection_filter = filters.regex(r"^check_connection$")
edit_client_setting_filter = filters.regex(r'^edit_clt(#.+|$)?$')
reload_settings_filter = filters.regex(r"^reload_settings$")


# Other
export_filter = filters.regex(r'^export(#.+|$)?$')
torrentInfo_filter = filters.regex(r'^torrentInfo(#.+|$)?$')
menu_filter = filters.regex(r"^menu$")
list_filter = filters.regex(r"^list$")
list_by_status_filter = filters.regex(r'^by_status_list(#.+|$)?$')
