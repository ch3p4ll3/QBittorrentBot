from pyrogram import Client
from pyrogram.errors.exceptions import MessageIdInvalid
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from typing import Optional

from ... import db_management
from ...configs import Configs
from ...client_manager import ClientRepo
from ...utils import get_user_from_config
from ...configs.enums import UserRolesEnum


async def send_menu(client: Client, message_id: int, chat_id: int) -> None:
    user = get_user_from_config(chat_id)
    buttons = [
        [InlineKeyboardButton("📝 List", "list")]
    ]

    if user.role in [UserRolesEnum.Manager, UserRolesEnum.Administrator]:
        buttons += [
            [InlineKeyboardButton("➕ Add Magnet", "category#add_magnet"),
             InlineKeyboardButton("➕ Add Torrent", "category#add_torrent")],
            [InlineKeyboardButton("⏯ Pause/Resume", "menu_pause_resume")]
        ]

    if user.role == UserRolesEnum.Administrator:
        buttons += [
            [InlineKeyboardButton("🗑 Delete", "menu_delete")],
            [InlineKeyboardButton("📂 Categories", "menu_categories")],
            [InlineKeyboardButton("⚙️ Settings", "settings")]
        ]

    db_management.write_support("None", chat_id)

    try:
        await client.edit_message_text(chat_id, message_id, text="Qbittorrent Control",
                                       reply_markup=InlineKeyboardMarkup(buttons))

    except MessageIdInvalid:
        await client.send_message(chat_id, text="Qbittorrent Control", reply_markup=InlineKeyboardMarkup(buttons))


async def list_active_torrents(client: Client, chat_id, message_id, callback: Optional[str] = None, status_filter: str = None) -> None:
    repository = ClientRepo.get_client_manager(Configs.config.client.type)
    torrents = repository.get_torrent_info(status_filter=status_filter)

    def render_categories_buttons():
        return [
            InlineKeyboardButton(f"⏳ {'*' if status_filter == 'downloading' else ''} Downloading",
                                 "by_status_list#downloading"),
            InlineKeyboardButton(f"✔️ {'*' if status_filter == 'completed' else ''} Completed",
                                 "by_status_list#completed"),
            InlineKeyboardButton(f"⏸️ {'*' if status_filter == 'paused' else ''} Paused", "by_status_list#paused"),
        ]

    categories_buttons = render_categories_buttons()
    if not torrents:
        buttons = [categories_buttons, [InlineKeyboardButton("🔙 Menu", "menu")]]
        try:
            await client.edit_message_text(chat_id, message_id, "There are no torrents",
                                           reply_markup=InlineKeyboardMarkup(buttons))
        except MessageIdInvalid:
            await client.send_message(chat_id, "There are no torrents", reply_markup=InlineKeyboardMarkup(buttons))
        return

    buttons = [categories_buttons]

    if callback is not None:
        for key, i in enumerate(torrents):
            buttons.append([InlineKeyboardButton(i.name, f"{callback}#{i.info.hash}")])

        buttons.append([InlineKeyboardButton("🔙 Menu", "menu")])

        try:
            await client.edit_message_reply_markup(chat_id, message_id, reply_markup=InlineKeyboardMarkup(buttons))
        except MessageIdInvalid:
            await client.send_message(chat_id, "Qbittorrent Control", reply_markup=InlineKeyboardMarkup(buttons))

    else:
        for key, i in enumerate(torrents):
            buttons.append([InlineKeyboardButton(i.name, f"torrentInfo#{i.info.hash}")])

        buttons.append([InlineKeyboardButton("🔙 Menu", "menu")])

        try:
            await client.edit_message_reply_markup(chat_id, message_id, reply_markup=InlineKeyboardMarkup(buttons))
        except MessageIdInvalid:
            await client.send_message(chat_id, "Qbittorrent Control", reply_markup=InlineKeyboardMarkup(buttons))
