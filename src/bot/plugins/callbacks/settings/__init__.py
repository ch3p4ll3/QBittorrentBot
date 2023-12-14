from pyrogram import Client
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from .... import custom_filters


@Client.on_callback_query(custom_filters.settings_filter)
async def settings_callback(client: Client, callback_query: CallbackQuery) -> None:
    await callback_query.edit_message_text(
        "QBittorrentBot Settings",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🫂 Users Settings", "get_users")
                ],
                [
                    InlineKeyboardButton("📥 Client Settings", "menu")
                ],
                [
                    InlineKeyboardButton("🇮🇹 Language Settings", "menu")
                ],
                [
                    InlineKeyboardButton("🔄 Reload Settings", "menu")
                ],
                [
                    InlineKeyboardButton("🔙 Menu", "menu")
                ]
            ]
        )
    )
