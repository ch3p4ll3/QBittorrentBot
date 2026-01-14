from pyrogram import Client
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from ....filters import custom_filters
from .....settings.user import User
from .....utils import inject_user
from .....translator import Translator, Strings


@Client.on_callback_query(custom_filters.settings_filter & custom_filters.check_user_filter & custom_filters.user_is_administrator)
@inject_user
async def settings_callback(client: Client, callback_query: CallbackQuery, user: User) -> None:
    await callback_query.edit_message_text(
        Translator.translate(Strings.SettingsMenu, user.locale),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(Translator.translate(Strings.UsersSettings, user.locale), "get_users")
                ],
                [
                    InlineKeyboardButton(Translator.translate(Strings.ClientSettings, user.locale), "edit_client")
                ],
                [
                    InlineKeyboardButton(Translator.translate(Strings.ReloadSettings, user.locale), "reload_settings")
                ],
                [
                    InlineKeyboardButton(Translator.translate(Strings.BackToMenu, user.locale), "menu")
                ]
            ]
        )
    )
