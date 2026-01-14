from typing import Optional
import logging

from aiogram import Bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from redis_helper.wrapper import RedisWrapper
from settings import Settings
from client_manager import ClientRepo
from utils import get_user_from_config
from settings.enums import UserRolesEnum
from translator import Translator, Strings
from ..filters.callbacks import CategoryAction, CategoryMenu

logger = logging.getLogger(__name__)


async def send_menu(bot: Bot, redis: RedisWrapper, settings: Settings, chat_id: int, message_id: Optional[int] = None) -> None:
    user = get_user_from_config(chat_id, settings)
    
    # Build buttons
    buttons = [
        [InlineKeyboardButton(text=Translator.translate(Strings.MenuList, user.locale), callback_data="list")]
    ]

    if user.role in [UserRolesEnum.Manager, UserRolesEnum.Administrator]:
        buttons += [
            [
                InlineKeyboardButton(
                    text=Translator.translate(Strings.AddMagnet, user.locale),
                    callback_data=CategoryAction(action="add_magnet").pack()
                ),
                InlineKeyboardButton(
                    text=Translator.translate(Strings.AddTorrent, user.locale),
                    callback_data=CategoryAction(action="add_torrent").pack()
                )
            ],
            [InlineKeyboardButton(text=Translator.translate(Strings.PauseResume, user.locale), callback_data="menu_pause_resume")]
        ]

    if user.role == UserRolesEnum.Administrator:
        buttons += [
            [InlineKeyboardButton(text=Translator.translate(Strings.Delete, user.locale), callback_data="menu_delete")],
            [InlineKeyboardButton(text=Translator.translate(Strings.Categories, user.locale), callback_data=CategoryMenu().pack())],
            [InlineKeyboardButton(text=Translator.translate(Strings.Settings, user.locale), callback_data="settings")]
        ]

    await redis.set(f"action:{chat_id}", None)
    markup = InlineKeyboardMarkup(inline_keyboard=buttons)

    try:
        if message_id:
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=Translator.translate(Strings.Menu, user.locale),
                reply_markup=markup
            )
        else:
            await bot.send_message(
                chat_id=chat_id,
                text=Translator.translate(Strings.Menu, user.locale),
                reply_markup=markup
            )
    except Exception as e:
        logger.warning(f"Failed to edit menu message, sending new one: {e}")
        await bot.send_message(
            chat_id=chat_id,
            text=Translator.translate(Strings.Menu, user.locale),
            reply_markup=markup
        )


async def list_active_torrents(
    bot: Bot,
    chat_id: int,
    message_id: int,
    callback: Optional[str] = None,
    status_filter: Optional[str] = None
) -> None:
    user = get_user_from_config(chat_id)
    repository = ClientRepo.get_client_manager(Settings.client.type)
    torrents = repository.get_torrents(status_filter=status_filter)

    # Status filter buttons
    categories_buttons = [
        InlineKeyboardButton(
            text=Translator.translate(Strings.ListFilterDownloading, user.locale, active='*' if status_filter == 'downloading' else ''),
            callback_data="by_status_list#downloading"
        ),
        InlineKeyboardButton(
            text=Translator.translate(Strings.ListFilterCompleted, user.locale, active='*' if status_filter == 'completed' else ''),
            callback_data="by_status_list#completed"
        ),
        InlineKeyboardButton(
            text=Translator.translate(Strings.ListFilterPaused, user.locale, active='*' if status_filter == 'paused' else ''),
            callback_data="by_status_list#paused"
        )
    ]

    buttons = [categories_buttons]

    if not torrents:
        buttons.append([InlineKeyboardButton(text=Translator.translate(Strings.BackToMenu, user.locale), callback_data="menu")])
        try:
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=Translator.translate(Strings.NoTorrents, user.locale),
                reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
            )
        except Exception:
            await bot.send_message(
                chat_id=chat_id,
                text=Translator.translate(Strings.NoTorrents, user.locale),
                reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
            )
        return

    # Torrent buttons
    for torrent in torrents:
        if callback:
            buttons.append([InlineKeyboardButton(text=torrent.name, callback_data=f"{callback}#{torrent.hash}")])
        else:
            buttons.append([InlineKeyboardButton(text=torrent.name, callback_data=f"torrentInfo#{torrent.hash}")])

    buttons.append([InlineKeyboardButton(text=Translator.translate(Strings.BackToMenu, user.locale), callback_data="menu")])
    markup = InlineKeyboardMarkup(inline_keyboard=buttons)

    try:
        await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=markup)
    except Exception:
        # fallback: send a new message
        await bot.send_message(
            chat_id=chat_id,
            text=Translator.translate(Strings.Menu, user.locale),
            reply_markup=markup
        )
