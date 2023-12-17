from pyrogram import Client
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from .... import custom_filters


@Client.on_callback_query(custom_filters.menu_category_filter & custom_filters.check_user_filter & custom_filters.user_is_administrator)
async def menu_category_callback(client: Client, callback_query: CallbackQuery) -> None:
    await callback_query.edit_message_text(
        "Pause/Resume a download",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("➕ Add Category", "add_category"),
                ],
                [
                    InlineKeyboardButton("🗑 Remove Category", "select_category#remove_category")
                ],
                [
                    InlineKeyboardButton("📝 Modify Category", "select_category#modify_category")],
                [
                    InlineKeyboardButton("🔙 Menu", "menu")
                ]
            ]
        )
    )





