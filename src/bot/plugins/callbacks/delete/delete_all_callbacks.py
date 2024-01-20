from pyrogram import Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from .... import custom_filters
from .....client_manager import ClientRepo
from ...common import send_menu
from .....configs import Configs

from .....configs.user import User
from .....utils import inject_user
from .....translator import Translator, Strings



@Client.on_callback_query(custom_filters.delete_all_filter & custom_filters.check_user_filter & custom_filters.user_is_administrator)
@inject_user
async def delete_all_callback(client: Client, callback_query: CallbackQuery, user: User) -> None:
    buttons = [
        [
            InlineKeyboardButton(Translator.translate(Strings.DeleteAllBtn, user.locale), "delete_all_no_data")
        ],
        [
            InlineKeyboardButton(Translator.translate(Strings.DeleteAllData, user.locale), "delete_all_data")
        ],
        [
            InlineKeyboardButton(Translator.translate(Strings.BackToMenu, user.locale), "menu")
        ]
    ]

    await client.edit_message_reply_markup(callback_query.from_user.id, callback_query.message.id,
                                           reply_markup=InlineKeyboardMarkup(buttons))


@Client.on_callback_query(custom_filters.delete_all_no_data_filter & custom_filters.check_user_filter & custom_filters.user_is_administrator)
@inject_user
async def delete_all_with_no_data_callback(client: Client, callback_query: CallbackQuery, user: User) -> None:
    repository = ClientRepo.get_client_manager(Configs.config.client.type)
    repository.delete_all_no_data()

    await client.answer_callback_query(callback_query.id, Translator.translate(Strings.DeletedAll, user.locale))
    await send_menu(client, callback_query.message.id, callback_query.from_user.id)


@Client.on_callback_query(custom_filters.delete_all_data_filter & custom_filters.check_user_filter & custom_filters.user_is_administrator)
@inject_user
async def delete_all_with_data_callback(client: Client, callback_query: CallbackQuery, user: User) -> None:
    repository = ClientRepo.get_client_manager(Configs.config.client.type)
    repository.delete_all_data()

    await client.answer_callback_query(callback_query.id, Translator.translate(Strings.DeletedAllData, user.locale))
    await send_menu(client, callback_query.message.id, callback_query.from_user.id)
