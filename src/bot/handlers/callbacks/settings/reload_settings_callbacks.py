from pyrogram import Client
from pyrogram.types import CallbackQuery

from ....filters import custom_filters
from .....settings import Configs
from .....settings.user import User
from .....utils import inject_user
from .....translator import Translator, Strings


@Client.on_callback_query(custom_filters.reload_settings_filter & custom_filters.check_user_filter & custom_filters.user_is_administrator)
@inject_user
async def reload_settings_callback(client: Client, callback_query: CallbackQuery, user: User) -> None:
    Configs.reload_config()
    await callback_query.answer(Translator.translate(Strings.SettingsReloaded, user.locale), show_alert=True)
