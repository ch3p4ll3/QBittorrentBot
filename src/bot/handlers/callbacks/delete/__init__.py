from pyrogram import Client
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from .... import custom_filters
from .....settings.user import User
from .....utils import inject_user
from .....translator import Translator, Strings


@Client.on_callback_query(custom_filters.menu_delete_filter & custom_filters.check_user_filter & custom_filters.user_is_administrator)
@inject_user
async def menu_delete_callback(client: Client, callback_query: CallbackQuery, user: User) -> None:
    await callback_query.edit_message_text(
        "Delete a torrent",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(Translator.translate(Strings.DeleteTorrentBtn, user.locale), "delete_one")
                ],
                [
                    InlineKeyboardButton(Translator.translate(Strings.DeleteAllMenuBtn, user.locale), "delete_all")
                ],
                [
                    InlineKeyboardButton(Translator.translate(Strings.BackToMenu, user.locale), "menu")
                ]
            ]
        )
    )
