from pyrogram import Client
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from .... import custom_filters
from .....utils import get_user_from_config
from .....configs import Configs

BOT_CONFIGS = Configs.load_config()


@Client.on_callback_query(custom_filters.get_users_filter)
async def get_users_callback(client: Client, callback_query: CallbackQuery) -> None:
    users = [
        [InlineKeyboardButton(f"User #{i.user_id}", f"user_info#{i.user_id}")]
        for i in BOT_CONFIGS.users
    ]

    await callback_query.edit_message_text(
        "Authorized users",
        reply_markup=InlineKeyboardMarkup(
            users +
            [
                [
                    InlineKeyboardButton("🔙 Menu", "menu")
                ]
            ]
        )
    )


@Client.on_callback_query(custom_filters.user_info_filter)
async def get_user_info_callback(client: Client, callback_query: CallbackQuery) -> None:
    user_id = int(callback_query.data.split("#")[1])

    user_info = get_user_from_config(user_id)

    # get all fields of the model dynamically
    fields = [
        [InlineKeyboardButton(f"Edit {key.replace('_', ' ').capitalize()}", f"edit_user#{user_id}-{key}-{item.annotation}")]
        for key, item in user_info.model_fields.items()
    ]

    await callback_query.edit_message_text(
        f"Edit User #{user_id}",
        reply_markup=InlineKeyboardMarkup(
            fields +
            [
                [
                    InlineKeyboardButton("🔙 Menu", "menu")
                ]
            ]
        )
    )


@Client.on_callback_query(custom_filters.edit_user_filter)
async def edit_user_callback(client: Client, callback_query: CallbackQuery) -> None:
    data = callback_query.data.split("#")[1]
    user_id = int(data.split("-")[0])
    field_to_edit = data.split("-")[1]
    data_type = data.split("-")[2]

    await callback_query.edit_message_text(
        f"Edit User #{user_id}",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🔙 Menu", "menu")
                ]
            ]
        )
    )
