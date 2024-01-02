import typing

from pyrogram import Client
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from .... import custom_filters
from .....configs import Configs
from .....db_management import write_support
from .....utils import get_user_from_config, convert_type_from_string


@Client.on_callback_query(custom_filters.get_users_filter & custom_filters.check_user_filter & custom_filters.user_is_administrator)
async def get_users_callback(client: Client, callback_query: CallbackQuery) -> None:
    users = [
        [InlineKeyboardButton(f"User #{i.user_id}", f"user_info#{i.user_id}")]
        for i in Configs.config.users
    ]

    await callback_query.edit_message_text(
        "Authorized users",
        reply_markup=InlineKeyboardMarkup(
            users +
            [
                [
                    InlineKeyboardButton("🔙 Settings", "settings")
                ]
            ]
        )
    )


@Client.on_callback_query(custom_filters.user_info_filter & custom_filters.check_user_filter & custom_filters.user_is_administrator)
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

    confs = '\n- '.join(iter([f"**{key.capitalize()}:** {item}" for key, item in user_info.model_dump().items()]))

    await callback_query.edit_message_text(
        f"Edit User #{user_id}\n\n**Current Settings:**\n- {confs}",
        reply_markup=InlineKeyboardMarkup(
            fields +
            [
                [
                    InlineKeyboardButton("🔙 Users", "get_users")
                ]
            ]
        )
    )


@Client.on_callback_query(custom_filters.edit_user_filter & custom_filters.check_user_filter & custom_filters.user_is_administrator)
async def edit_user_callback(client: Client, callback_query: CallbackQuery) -> None:
    data = callback_query.data.split("#")[1]
    user_id = int(data.split("-")[0])
    field_to_edit = data.split("-")[1]
    data_type = convert_type_from_string(data.split("-")[2])

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
                        InlineKeyboardButton(f"🔙 User#{user_id} info", f"user_info#{user_id}")
                    ]
                ]
            )
        )

        return

    write_support(callback_query.data, callback_query.from_user.id)

    await callback_query.edit_message_text(
        f"Send the new value for field \"{field_to_edit}\" for user #{user_id}. \n\n**Note:** the field type is \"{data_type}\"",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(f"🔙 User#{user_id} info", f"user_info#{user_id}")
                ]
            ]
        )
    )


@Client.on_callback_query(custom_filters.toggle_user_var_filter & custom_filters.check_user_filter & custom_filters.user_is_administrator)
async def toggle_user_var(client: Client, callback_query: CallbackQuery) -> None:
    data = callback_query.data.split("#")[1]
    user_id = int(data.split("-")[0])
    field_to_edit = data.split("-")[1]

    user_info = get_user_from_config(user_id)
    user_from_configs = Configs.config.users.index(user_info)

    if user_from_configs == -1:
        return

    Configs.config.users[user_from_configs].notify = not Configs.config.users[user_from_configs].notify
    Configs.update_config(Configs.config)

    await callback_query.edit_message_text(
        f"Edit User #{user_id} {field_to_edit} Field",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        f"{'✅' if Configs.config.users[user_from_configs].notify else '❌'} Toggle",
                        f"toggle_user_var#{user_id}-{field_to_edit}")
                ],
                [
                    InlineKeyboardButton(f"🔙 User#{user_id} info", f"user_info#{user_id}")
                ]
            ]
        )
    )
