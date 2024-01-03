from pyrogram import Client
from pyrogram.errors.exceptions import MessageIdInvalid
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from typing import Optional

from ... import db_management
from ...configs import Configs
from ...client_manager import ClientRepo
from ...utils import get_user_from_config
from ...configs.enums import UserRolesEnum
from ...translator import Translator, Strings


async def send_menu(client: Client, message_id: int, chat_id: int) -> None:
    user = get_user_from_config(chat_id)
    buttons = [
        [InlineKeyboardButton(Translator.translate(Strings.MenuList, user.locale), "list")]
    ]

    if user.role in [UserRolesEnum.Manager, UserRolesEnum.Administrator]:
        buttons += [
            [InlineKeyboardButton(Translator.translate(Strings.AddMagnet, user.locale), "category#add_magnet"),
             InlineKeyboardButton(Translator.translate(Strings.AddTorrent, user.locale), "category#add_torrent")],
            [InlineKeyboardButton(Translator.translate(Strings.PauseResume, user.locale), "menu_pause_resume")]
        ]

    if user.role == UserRolesEnum.Administrator:
        buttons += [
            [InlineKeyboardButton(Translator.translate(Strings.Delete, user.locale), "menu_delete")],
            [InlineKeyboardButton(Translator.translate(Strings.Categories, user.locale), "menu_categories")],
            [InlineKeyboardButton(Translator.translate(Strings.Settings, user.locale), "settings")]
        ]

    db_management.write_support("None", chat_id)

    try:
        await client.edit_message_text(chat_id, message_id, text=Translator.translate(Strings.Menu, user.locale),
                                       reply_markup=InlineKeyboardMarkup(buttons))

    except MessageIdInvalid:
        await client.send_message(
            chat_id,
            text=Translator.translate(Strings.Menu, user.locale),
            reply_markup=InlineKeyboardMarkup(buttons)
        )


async def list_active_torrents(client: Client, chat_id: int, message_id: int, callback: Optional[str] = None, status_filter: str = None) -> None:
    user = get_user_from_config(chat_id)
    repository = ClientRepo.get_client_manager(Configs.config.client.type)
    torrents = repository.get_torrent_info(status_filter=status_filter)

    def render_categories_buttons():
        return [
            InlineKeyboardButton(
                Translator.translate(
                    Strings.ListFilterDownloading, user.locale, active='*' if status_filter == 'downloading' else ''
                ),
                "by_status_list#downloading"
            ),

            InlineKeyboardButton(
                Translator.translate(
                    Strings.ListFilterCompleted, user.locale, active='*' if status_filter == 'completed' else ''
                ),
                "by_status_list#completed"
            ),

            InlineKeyboardButton(
                Translator.translate(
                    Strings.ListFilterPaused, user.locale, active='*' if status_filter == 'paused' else ''
                ),
                "by_status_list#paused"
            ),
        ]

    categories_buttons = render_categories_buttons()
    if not torrents:
        buttons = [
            categories_buttons,
            [
                InlineKeyboardButton(Translator.translate(Strings.BackToMenu, user.locale), "menu")
            ]
        ]

        try:
            await client.edit_message_text(
                chat_id,
                message_id,
                Translator.translate(Strings.NoTorrents, user.locale),
                reply_markup=InlineKeyboardMarkup(buttons)
            )

        except MessageIdInvalid:
            await client.send_message(
                chat_id,
                Translator.translate(Strings.NoTorrents, user.locale),
                reply_markup=InlineKeyboardMarkup(buttons)
            )

        return

    buttons = [categories_buttons]

    if callback is not None:
        for key, i in enumerate(torrents):
            buttons.append([InlineKeyboardButton(i.name, f"{callback}#{i.info.hash}")])

    else:
        for _, i in enumerate(torrents):
            buttons.append([InlineKeyboardButton(i.name, f"torrentInfo#{i.info.hash}")])

    buttons.append(
        [
            InlineKeyboardButton(Translator.translate(Strings.BackToMenu, user.locale), "menu")
        ]
    )

    try:
        await client.edit_message_reply_markup(chat_id, message_id, reply_markup=InlineKeyboardMarkup(buttons))
    except MessageIdInvalid:
        await client.send_message(
            chat_id,
            Translator.translate(Strings.Menu, user.locale),
            reply_markup=InlineKeyboardMarkup(buttons)
        )
