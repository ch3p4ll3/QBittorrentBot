from pyrogram import Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.errors.exceptions import MessageIdInvalid

from . import add_magnet_callback, add_torrent_callback
from .... import db_management
from ... import custom_filters
from ....qbittorrent_manager import QbittorrentManagement


@Client.on_callback_query(custom_filters.add_category_filter & custom_filters.check_user_filter & (custom_filters.user_is_administrator | custom_filters.user_is_manager))
async def add_category_callback(client: Client, callback_query: CallbackQuery) -> None:
    db_management.write_support("category_name", callback_query.from_user.id)
    button = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Menu", "menu")]])
    try:
        await client.edit_message_text(callback_query.from_user.id, callback_query.message.id,
                                       "Send the category name", reply_markup=button)
    except MessageIdInvalid:
        await client.send_message(callback_query.from_user.id, "Send the category name", reply_markup=button)


@Client.on_callback_query(custom_filters.select_category_filter & custom_filters.check_user_filter & (custom_filters.user_is_administrator | custom_filters.user_is_manager))
async def list_categories(client: Client, callback_query: CallbackQuery):
    buttons = []

    with QbittorrentManagement() as qb:
        categories = qb.get_categories()

    if categories is None:
        buttons.append([InlineKeyboardButton("🔙 Menu", "menu")])
        await client.edit_message_text(callback_query.from_user.id, callback_query.message.id,
                                       "There are no categories", reply_markup=InlineKeyboardMarkup(buttons))
        return

    for key, i in enumerate(categories):
        buttons.append([InlineKeyboardButton(i, f"{callback_query.data.split('#')[1]}#{i}")])

    buttons.append([InlineKeyboardButton("🔙 Menu", "menu")])

    try:
        await client.edit_message_text(callback_query.from_user.id, callback_query.message.id,
                                       "Choose a category:", reply_markup=InlineKeyboardMarkup(buttons))
    except MessageIdInvalid:
        await client.send_message(callback_query.from_user.id, "Choose a category:",
                                  reply_markup=InlineKeyboardMarkup(buttons))


@Client.on_callback_query(custom_filters.remove_category_filter & custom_filters.check_user_filter & custom_filters.user_is_administrator)
async def remove_category_callback(client: Client, callback_query: CallbackQuery) -> None:
    buttons = [[InlineKeyboardButton("🔙 Menu", "menu")]]

    with QbittorrentManagement() as qb:
        qb.remove_category(callback_query.data.split("#")[1])

    await client.edit_message_text(callback_query.from_user.id, callback_query.message.id,
                                   f"The category {callback_query.data.split('#')[1]} has been removed",
                                   reply_markup=InlineKeyboardMarkup(buttons))


@Client.on_callback_query(custom_filters.modify_category_filter & custom_filters.check_user_filter & custom_filters.user_is_administrator)
async def modify_category_callback(client: Client, callback_query: CallbackQuery) -> None:
    buttons = [[InlineKeyboardButton("🔙 Menu", "menu")]]

    db_management.write_support(f"category_dir_modify#{callback_query.data.split('#')[1]}", callback_query.from_user.id)
    await client.edit_message_text(callback_query.from_user.id, callback_query.message.id,
                                   f"Send new path for category {callback_query.data.split('#')[1]}",
                                   reply_markup=InlineKeyboardMarkup(buttons))


@Client.on_callback_query(custom_filters.category_filter & custom_filters.check_user_filter & (custom_filters.user_is_administrator | custom_filters.user_is_manager))
async def category(client: Client, callback_query: CallbackQuery) -> None:
    buttons = []

    with QbittorrentManagement() as qb:
        categories = qb.get_categories()

    if categories is None:
        if "magnet" in callback_query.data:
            await add_magnet_callback(client, callback_query)

        else:
            await add_torrent_callback(client, callback_query)

        return

    for key, i in enumerate(categories):
        buttons.append([InlineKeyboardButton(i, f"{callback_query.data.split('#')[1]}#{i}")])

    buttons.append([InlineKeyboardButton("None", f"{callback_query.data.split('#')[1]}#None")])
    buttons.append([InlineKeyboardButton("🔙 Menu", "menu")])

    try:
        await client.edit_message_text(callback_query.from_user.id, callback_query.message.id,
                                       "Choose a category:", reply_markup=InlineKeyboardMarkup(buttons))
    except MessageIdInvalid:
        await client.send_message(callback_query.from_user.id, "Choose a category:",
                                  reply_markup=InlineKeyboardMarkup(buttons))
