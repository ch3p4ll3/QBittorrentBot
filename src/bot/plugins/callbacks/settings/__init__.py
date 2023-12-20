from pyrogram import Client
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from .... import custom_filters


@Client.on_callback_query(custom_filters.settings_filter & custom_filters.check_user_filter & custom_filters.user_is_administrator)
async def settings_callback(client: Client, callback_query: CallbackQuery) -> None:
    await callback_query.edit_message_text(
        "QBittorrentBot Settings",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🫂 Users Settings", "get_users")
                ],
                [
                    InlineKeyboardButton("📥 Client Settings", "edit_client")
                ],
                [
                    InlineKeyboardButton("🇮🇹 Language Settings", "menu")
                ],
                [
                    InlineKeyboardButton("🔄 Reload Settings", "reload_settings")
                ],
                [
                    InlineKeyboardButton("🔙 Menu", "menu")
                ]
            ]
        )
    )
