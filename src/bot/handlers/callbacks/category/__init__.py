from pyrogram import Client
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from ....filters import custom_filters
from .....settings.user import User
from .....utils import inject_user
from .....translator import Translator, Strings


@Client.on_callback_query(custom_filters.menu_category_filter & custom_filters.check_user_filter & custom_filters.user_is_administrator)
@inject_user
async def menu_category_callback(client: Client, callback_query: CallbackQuery, user: User) -> None:
    await callback_query.edit_message_text(
        "Pause/Resume a download",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(Translator.translate(Strings.AddCategory, user.locale), "add_category"),
                ],
                [
                    InlineKeyboardButton(Translator.translate(Strings.RemoveCategory, user.locale), "select_category#remove_category")
                ],
                [
                    InlineKeyboardButton(Translator.translate(Strings.EditCategory, user.locale), "select_category#modify_category")],
                [
                    InlineKeyboardButton(Translator.translate(Strings.BackToMenu, user.locale), "menu")
                ]
            ]
        )
    )





