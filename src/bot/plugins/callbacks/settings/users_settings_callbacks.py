import typing

from pyrogram import Client
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from .... import custom_filters
from .....configs import Configs
from .....db_management import write_support
from .....utils import get_user_from_config

BOT_CONFIGS = Configs.config


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

    write_support("None", callback_query.from_user.id)

    # get all fields of the model dynamically
    fields = [
        [InlineKeyboardButton(f"Edit {key.replace('_', ' ').capitalize()}",
                              f"edit_user#{user_id}-{key}-{item.annotation}")]
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
    data_type = eval(data.split("-")[2].replace("<class ", "").replace(">", ""))

    user_info = get_user_from_config(user_id)

    if data_type == bool or data_type == typing.Optional[bool]:
        await callback_query.edit_message_text(
            f"Edit User #{user_id} {field_to_edit} Field",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            f"{'✅' if user_info.notify else '❌'} Toggle",
                            f"toggle_user_var#{user_id}-{field_to_edit}")
                    ],
                    [
                        InlineKeyboardButton("🔙 Menu", f"user_info#{user_id}")
                    ]
                ]
            )
        )

        return

    write_support(callback_query.data, callback_query.from_user.id)

    await callback_query.edit_message_text(
        f"Send the new value for {field_to_edit} for user #{user_id}. \n\n**Note:** the field type is {data_type}",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🔙 Menu", f"user_info#{user_id}")
                ]
            ]
        )
    )


@Client.on_callback_query(custom_filters.toggle_user_var_filter)
async def toggle_user_var(client: Client, callback_query: CallbackQuery) -> None:
    data = callback_query.data.split("#")[1]
    user_id = int(data.split("-")[0])
    field_to_edit = data.split("-")[1]

    user_info = get_user_from_config(user_id)
    user_from_configs = BOT_CONFIGS.users.index(user_info)

    if user_from_configs == -1:
        return

    BOT_CONFIGS.users[user_from_configs].notify = not BOT_CONFIGS.users[user_from_configs].notify
    Configs.update_config(BOT_CONFIGS)

    await callback_query.edit_message_text(
        f"Edit User #{user_id} {field_to_edit} Field",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        f"{'✅' if BOT_CONFIGS.users[user_from_configs].notify else '❌'} Toggle",
                        f"toggle_user_var#{user_id}-{field_to_edit}")
                ],
                [
                    InlineKeyboardButton("🔙 Menu", f"user_info#{user_id}")
                ]
            ]
        )
    )
