from aiogram.filters import BaseFilter
from aiogram.types import Message
from aiogram.types import CallbackQuery

from settings import Settings
from utils import get_user_from_config
from settings.enums import UserRolesEnum

from aiogram import F as filters


# Authorization filters
class IsAuthorizedUser(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        allowed_ids = {i.user_id for i in Settings.users}
        return message.from_user.id in allowed_ids


class HasRole(BaseFilter):
    def __init__(self, role: UserRolesEnum):
        self.role = role

    async def __call__(self, query: CallbackQuery) -> bool:
        user = get_user_from_config(query.from_user.id)
        return user and user.role == self.role


# Categories filters
menu_category_filter = filters.regexp(r"^menu_categories$")
add_category_filter = filters.regexp(r"^add_category$")
remove_category_filter = filters.regexp(r'^remove_category(#.+|$)?$')
modify_category_filter = filters.regexp(r'^modify_category(#.+|$)?$')
category_filter = filters.regexp(r'^category(#.+|$)?$')
select_category_filter = filters.regexp(r'^select_category(#.+|$)?$')

# Add filters
add_magnet_filter = filters.regexp(r'^add_magnet(#.+|$)?$')
add_torrent_filter = filters.regexp(r'^add_torrent(#.+|$)?$')

# Pause/Resume filters
menu_pause_resume_filter = filters.regexp(r"^menu_pause_resume$")
pause_all_filter = filters.regexp(r"^pause_all$")
resume_all_filter = filters.regexp(r"^resume_all$")
pause_filter = filters.regexp(r'^pause(#.+|$)?$')
resume_filter = filters.regexp(r'^resume(#.+|$)?$')

# Delete filers
menu_delete_filter = filters.regexp(r"^menu_delete$")
delete_one_filter = filters.regexp(r'^delete_one(#.+|$)?$')
delete_one_no_data_filter = filters.regexp(r'^delete_one_no_data(#.+|$)?$')
delete_one_data_filter = filters.regexp(r'^delete_one_data(#.+|$)?$')
delete_all_filter = filters.regexp(r'^delete_all(#.+|$)?$')
delete_all_no_data_filter = filters.regexp(r"^delete_all_no_data$")
delete_all_data_filter = filters.regexp(r"^delete_all_data$")

# Settings filters
settings_filter = filters.regexp(r"^settings$")
get_users_filter = filters.regexp(r"^get_users$")
user_info_filter = filters.regexp(r'^user_info(#.+|$)?$')
edit_user_filter = filters.regexp(r'^edit_user(#.+|$)?$')
toggle_user_var_filter = filters.regexp(r'^toggle_user_var(#.+|$)?$')
edit_locale_filter = filters.regexp(r'^edit_locale(#.+|$)?$')
edit_client_settings_filter = filters.regexp(r"^edit_client$")
list_client_settings_filter = filters.regexp(r"^lst_client$")
check_connection_filter = filters.regexp(r"^check_connection$")
edit_client_setting_filter = filters.regexp(r'^edit_clt(#.+|$)?$')
reload_settings_filter = filters.regexp(r"^reload_settings$")
toggle_speed_limit_filter = filters.regexp(r"^toggle_speed_limit$")


# Other
export_filter = filters.regexp(r'^export(#.+|$)?$')
torrentInfo_filter = filters.regexp(r'^torrentInfo(#.+|$)?$')
menu_filter = filters.regexp(r"^menu$")
list_filter = filters.regexp(r"^list$")
list_by_status_filter = filters.regexp(r'^by_status_list(#.+|$)?$')
