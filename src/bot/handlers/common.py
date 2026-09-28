from typing import Optional
import logging

from aiogram import Bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.i18n import gettext as _

from src.redis_helper.wrapper import RedisWrapper
from src.settings import Settings
from src.client_manager.client_repo import ClientRepo
from src.utils import get_user_from_config
from src.settings.enums import UserRolesEnum
from src.bot.filters.callbacks import CategoryAction, CategoryMenu, ListByStatus, List, TorrentInfo, SettingsMenu, DeleteMenu, PauseResumeMenu, Menu

logger = logging.getLogger(__name__)


async def send_menu(bot: Bot, redis: RedisWrapper, settings: Settings, chat_id: int, message_id: Optional[int] = None) -> None:
    user = get_user_from_config(chat_id, settings)

    # Build buttons
    buttons = [
        [InlineKeyboardButton(text=_("📝 List"), callback_data=List().pack())]
    ]

    if user.role in [UserRolesEnum.Manager, UserRolesEnum.Administrator]:
        buttons += [
            [
                InlineKeyboardButton(
                    text=_("➕ Add Magnet"),
                    callback_data=CategoryAction(action="add_magnet").pack()
                ),
                InlineKeyboardButton(
                    text=_("➕ Add Torrent"),
                    callback_data=CategoryAction(action="add_torrent").pack()
                )
            ],
            [InlineKeyboardButton(text=_("⏯ Pause/Resume"), callback_data=PauseResumeMenu().pack())]
        ]

    if user.role == UserRolesEnum.Administrator:
        buttons += [
            [InlineKeyboardButton(text=_("🗑 Delete"), callback_data=DeleteMenu().pack())],
            [InlineKeyboardButton(text=_("📂 Categories"), callback_data=CategoryMenu().pack())],
            [InlineKeyboardButton(text=_("⚙️ Settings"), callback_data=SettingsMenu().pack())]
        ]

    await redis.delete(f"action:{chat_id}")
    markup = InlineKeyboardMarkup(inline_keyboard=buttons)

    try:
        if message_id:
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=_("Welcome to QBittorrent Bot"),
                reply_markup=markup
            )
        else:
            await bot.send_message(
                chat_id=chat_id,
                text=_("Welcome to QBittorrent Bot"),
                reply_markup=markup
            )
    except Exception as e:
        logger.warning(f"Failed to edit menu message, sending new one: {e}")
        await bot.send_message(
            chat_id=chat_id,
            text=_("Welcome to QBittorrent Bot"),
            reply_markup=markup
        )


async def list_active_torrents(
    bot: Bot,
    chat_id: int,
    message_id: int,
    settings: Settings,
    callback: Optional[str] = None,
    status_filter: Optional[str] = None
) -> None:
    repository_class = ClientRepo.get_client_manager(settings.client.type)
    torrents = await repository_class(settings).get_torrents(status_filter=status_filter)

    # Status filter buttons
    categories_buttons = [
        InlineKeyboardButton(
            text=_("⏳ {active} Downloading"
                .format(
                    active='*' if status_filter == 'downloading' else ''
                )
            ),
            callback_data=ListByStatus(status="downloading").pack()
        ),
        InlineKeyboardButton(
            text=_("✔️ {active} Completed"
                .format(
                    active='*' if status_filter == 'completed' else ''
                )
            ),
            callback_data=ListByStatus(status="completed").pack()
        ),
        InlineKeyboardButton(
            text=_("⏸️ {active} Paused"
                .format(
                    active='*' if status_filter == 'paused' else ''
                )
            ),
            callback_data=ListByStatus(status="paused").pack()
        )
    ]

    buttons = [categories_buttons]

    if not torrents:
        buttons.append([InlineKeyboardButton(text=_("🔙 Menu"), callback_data="menu")])
        try:
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=_("There are no torrents"),
                reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
            )
        except Exception:
            await bot.send_message(
                chat_id=chat_id,
                text=_("There are no torrents"),
                reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
            )
        return

    # Torrent buttons
    for torrent in torrents:
        if callback:
            buttons.append([InlineKeyboardButton(text=torrent.name[:40], callback_data=f"{callback}:{torrent.hash}")])
        else:
            buttons.append([InlineKeyboardButton(text=torrent.name[:40], callback_data=TorrentInfo(torrent_hash=torrent.hash).pack())])

    buttons.append([InlineKeyboardButton(text=_("🔙 Menu"), callback_data="menu")])
    markup = InlineKeyboardMarkup(inline_keyboard=buttons)

    try:
        await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=markup)
    except Exception:
        # fallback: send a new message
        await bot.send_message(
            chat_id=chat_id,
            text=_("🔙 Menu"),
            reply_markup=markup
        )


async def list_categories(
    bot: Bot,
    chat_id: int,
    message_id: int,
    settings: Settings,
    callback: str
):
    buttons = []

    repository_class_class = ClientRepo.get_client_manager(settings.client.type)
    categories = await repository_class_class(settings).get_categories()

    if categories is None:
        buttons.append([InlineKeyboardButton(text=_("🔙 Menu"), callback_data=Menu().pack())])

        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=_("There are no categories"),
            reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
        )

        return

    for i in categories:
        buttons.append([InlineKeyboardButton(text=i, callback_data=f"{callback}:{i}")])

    buttons.append([InlineKeyboardButton(text=_("🔙 Menu"), callback_data=Menu().pack())])

    try:
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=_("Choose a category:"),
            reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
        )

    except Exception:
        await bot.send_message(
            chat_id,
            _("Choose a category:"),
            reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
        )
