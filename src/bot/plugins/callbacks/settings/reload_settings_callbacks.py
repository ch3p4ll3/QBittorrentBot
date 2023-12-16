from pyrogram import Client
from pyrogram.types import CallbackQuery

from .... import custom_filters
from .....configs import Configs


@Client.on_callback_query(custom_filters.reload_settings_filter)
async def reload_settings_callback(client: Client, callback_query: CallbackQuery) -> None:
    # TO FIX reload
    Configs.reload_config()
    await callback_query.answer("Settings Reloaded", show_alert=True)
