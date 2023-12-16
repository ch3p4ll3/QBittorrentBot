from pyrogram import Client
from pyrogram.errors.exceptions import MessageIdInvalid
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from ... import db_management
from ...qbittorrent_manager import QbittorrentManagement
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
            [InlineKeyboardButton("⏸ Pause", "pause"),
             InlineKeyboardButton("▶️ Resume", "resume")],
            [InlineKeyboardButton("⏸ Pause All", "pause_all"),
             InlineKeyboardButton("▶️ Resume All", "resume_all")],
        ]

    if user.role == UserRolesEnum.Administrator:
        buttons += [
            [InlineKeyboardButton("🗑 Delete", "delete_one"),
             InlineKeyboardButton("🗑 Delete All", "delete_all")],
            [InlineKeyboardButton("➕ Add Category", "add_category"),
             InlineKeyboardButton("🗑 Remove Category", "select_category#remove_category")],
            [InlineKeyboardButton("📝 Modify Category", "select_category#modify_category")],
            [InlineKeyboardButton("⚙️ Settings", "settings")]
        ]

    db_management.write_support("None", chat_id)

    try:
        await client.edit_message_text(chat_id, message_id, text="Qbittorrent Control",
                                       reply_markup=InlineKeyboardMarkup(buttons))

    except MessageIdInvalid:
        await client.send_message(chat_id, text="Qbittorrent Control", reply_markup=InlineKeyboardMarkup(buttons))


async def list_active_torrents(client: Client, n, chat, message, callback, status_filter: str = None) -> None:
    with QbittorrentManagement() as qb:
        torrents = qb.get_torrent_info(status_filter=status_filter)

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
            await client.edit_message_text(chat, message, "There are no torrents",
                                           reply_markup=InlineKeyboardMarkup(buttons))
        except MessageIdInvalid:
            await client.send_message(chat, "There are no torrents", reply_markup=InlineKeyboardMarkup(buttons))
        return

    buttons = [categories_buttons]

    if n == 1:
        for key, i in enumerate(torrents):
            buttons.append([InlineKeyboardButton(i.name, f"{callback}#{i.info.hash}")])

        buttons.append([InlineKeyboardButton("🔙 Menu", "menu")])

        try:
            await client.edit_message_reply_markup(chat, message, reply_markup=InlineKeyboardMarkup(buttons))
        except MessageIdInvalid:
            await client.send_message(chat, "Qbittorrent Control", reply_markup=InlineKeyboardMarkup(buttons))

    else:
        for key, i in enumerate(torrents):
            buttons.append([InlineKeyboardButton(i.name, f"torrentInfo#{i.info.hash}")])

        buttons.append([InlineKeyboardButton("🔙 Menu", "menu")])

        try:
            await client.edit_message_reply_markup(chat, message, reply_markup=InlineKeyboardMarkup(buttons))
        except MessageIdInvalid:
            await client.send_message(chat, "Qbittorrent Control", reply_markup=InlineKeyboardMarkup(buttons))
