from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery

from settings import Settings
from utils import get_user_from_config
from settings.enums import UserRolesEnum

from aiogram import F as filters


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
