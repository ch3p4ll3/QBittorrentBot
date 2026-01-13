from pyrogram import Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.errors.exceptions import MessageIdInvalid

from ..add_torrents_callbacks import add_magnet_callback, add_torrent_callback
from ..... import db_management
from .... import custom_filters
from .....client_manager import ClientRepo
from .....settings import Configs

from .....settings.user import User
from .....utils import inject_user
from .....translator import Translator, Strings


@Client.on_callback_query(custom_filters.add_category_filter & custom_filters.check_user_filter & (custom_filters.user_is_administrator | custom_filters.user_is_manager))
@inject_user
async def add_category_callback(client: Client, callback_query: CallbackQuery, user: User) -> None:
    db_management.write_support("category_name", callback_query.from_user.id)
    button = InlineKeyboardMarkup([[InlineKeyboardButton(Translator.translate(Strings.BackToMenu, user.locale), "menu")]])
    try:
        await client.edit_message_text(
            callback_query.from_user.id,
            callback_query.message.id,
            Translator.translate(Strings.NewCategoryName, user.locale),
            reply_markup=button
        )

    except MessageIdInvalid:
        await client.send_message(
            callback_query.from_user.id,
            Translator.translate(Strings.NewCategoryName, user.locale),
            reply_markup=button
        )


@Client.on_callback_query(custom_filters.select_category_filter & custom_filters.check_user_filter & (custom_filters.user_is_administrator | custom_filters.user_is_manager))
@inject_user
async def list_categories(client: Client, callback_query: CallbackQuery, user: User):
    buttons = []

    repository = ClientRepo.get_client_manager(Configs.config.client.type)
    categories = repository.get_categories()

    if categories is None:
        buttons.append([InlineKeyboardButton(Translator.translate(Strings.BackToMenu, user.locale), "menu")])
        await client.edit_message_text(
            callback_query.from_user.id,
            callback_query.message.id,
            Translator.translate(Strings.NoCategory, user.locale),
            reply_markup=InlineKeyboardMarkup(buttons)
        )

        return

    for _, i in enumerate(categories):
        buttons.append([InlineKeyboardButton(i, f"{callback_query.data.split('#')[1]}#{i}")])

    buttons.append([InlineKeyboardButton(Translator.translate(Strings.BackToMenu, user.locale), "menu")])

    try:
        await client.edit_message_text(
            callback_query.from_user.id,
            callback_query.message.id,
            Translator.translate(Strings.ChooseCategory, user.locale),
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    except MessageIdInvalid:
        await client.send_message(
            callback_query.from_user.id,
            Translator.translate(Strings.ChooseCategory, user.locale),
            reply_markup=InlineKeyboardMarkup(buttons)
        )


@Client.on_callback_query(custom_filters.remove_category_filter & custom_filters.check_user_filter & custom_filters.user_is_administrator)
@inject_user
async def remove_category_callback(client: Client, callback_query: CallbackQuery, user: User) -> None:
    buttons = [[InlineKeyboardButton(Translator.translate(Strings.BackToMenu, user.locale), "menu")]]

    repository = ClientRepo.get_client_manager(Configs.config.client.type)
    repository.remove_category(callback_query.data.split("#")[1])

    await client.edit_message_text(
        callback_query.from_user.id,
        callback_query.message.id,
        Translator.translate(Strings.OnCategoryRemoved, user.locale, category_name=callback_query.data.split('#')[1]),
        reply_markup=InlineKeyboardMarkup(buttons)
    )


@Client.on_callback_query(custom_filters.modify_category_filter & custom_filters.check_user_filter & custom_filters.user_is_administrator)
@inject_user
async def modify_category_callback(client: Client, callback_query: CallbackQuery, user: User) -> None:
    buttons = [[InlineKeyboardButton(Translator.translate(Strings.BackToMenu, user.locale), "menu")]]

    db_management.write_support(f"category_dir_modify#{callback_query.data.split('#')[1]}", callback_query.from_user.id)
    await client.edit_message_text(
        callback_query.from_user.id,
        callback_query.message.id,
        Translator.translate(Strings.OnCategoryEdited, user.locale, category_name=callback_query.data.split('#')[1]),
        reply_markup=InlineKeyboardMarkup(buttons)
    )


@Client.on_callback_query(custom_filters.category_filter & custom_filters.check_user_filter & (custom_filters.user_is_administrator | custom_filters.user_is_manager))
@inject_user
async def category(client: Client, callback_query: CallbackQuery, user: User) -> None:
    buttons = []

    repository = ClientRepo.get_client_manager(Configs.config.client.type)
    categories = repository.get_categories()

    if categories is None:
        if "magnet" in callback_query.data:
            await add_magnet_callback(client, callback_query)

        else:
            await add_torrent_callback(client, callback_query)

        return

    for _, i in enumerate(categories):
        buttons.append([InlineKeyboardButton(i, f"{callback_query.data.split('#')[1]}#{i}")])

    buttons.append([InlineKeyboardButton("None", f"{callback_query.data.split('#')[1]}#None")])
    buttons.append([InlineKeyboardButton(Translator.translate(Strings.BackToMenu, user.locale), "menu")])

    try:
        await client.edit_message_text(
            callback_query.from_user.id,
            callback_query.message.id,
            Translator.translate(Strings.ChooseCategory, user.locale),
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    except MessageIdInvalid:
        await client.send_message(
            callback_query.from_user.id,
            Translator.translate(Strings.ChooseCategory, user.locale),
            reply_markup=InlineKeyboardMarkup(buttons)
        )
