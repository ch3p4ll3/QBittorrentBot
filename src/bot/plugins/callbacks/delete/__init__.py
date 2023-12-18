from pyrogram import Client
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from .... import custom_filters


@Client.on_callback_query(custom_filters.menu_delete_filter & custom_filters.check_user_filter & custom_filters.user_is_administrator)
async def menu_delete_callback(client: Client, callback_query: CallbackQuery) -> None:
    await callback_query.edit_message_text(
        "Delete a torrent",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🗑 Delete", "delete_one")
                ],
                [
                    InlineKeyboardButton("🗑 Delete All", "delete_all")
                ],
                [
                    InlineKeyboardButton("🔙 Menu", "menu")
                ]
            ]
        )
    )
