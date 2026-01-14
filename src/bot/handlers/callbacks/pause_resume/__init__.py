from pyrogram import Client
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from ....filters import custom_filters
from .....settings.user import User
from .....utils import inject_user
from .....translator import Translator, Strings


@Client.on_callback_query(custom_filters.menu_pause_resume_filter & custom_filters.check_user_filter & custom_filters.user_is_administrator)
@inject_user
async def menu_pause_resume_callback(client: Client, callback_query: CallbackQuery, user: User) -> None:
    await callback_query.edit_message_text(
        Translator.translate(Strings.PauseResumeMenu, user.locale),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(Translator.translate(Strings.PauseTorrentBtn, user.locale), "pause"),
                    InlineKeyboardButton(Translator.translate(Strings.ResumeTorrentBtn, user.locale), "resume")
                ],
                [
                    InlineKeyboardButton(Translator.translate(Strings.PauseAll, user.locale), "pause_all"),
                    InlineKeyboardButton(Translator.translate(Strings.ResumeAll, user.locale), "resume_all")
                ],
                [
                    InlineKeyboardButton(Translator.translate(Strings.BackToMenu, user.locale), "menu")
                ]
            ]
        )
    )
