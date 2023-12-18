from pyrogram import Client
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from .... import custom_filters


@Client.on_callback_query(custom_filters.menu_pause_resume_filter & custom_filters.check_user_filter & custom_filters.user_is_administrator)
async def menu_pause_resume_callback(client: Client, callback_query: CallbackQuery) -> None:
    await callback_query.edit_message_text(
        "Pause/Resume a torrent",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⏸ Pause", "pause"),
                    InlineKeyboardButton("▶️ Resume", "resume")
                ],
                [
                    InlineKeyboardButton("⏸ Pause All", "pause_all"),
                    InlineKeyboardButton("▶️ Resume All", "resume_all")
                ],
                [
                    InlineKeyboardButton("🔙 Menu", "menu")
                ]
            ]
        )
    )
