from pyrogram import Client
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from varname import nameof

from .... import custom_filters
from .....configs import Configs
from .....configs.user import User
from .....db_management import write_support
from .....utils import get_user_from_config, convert_type_from_string, inject_user
from .....translator import Translator, Strings


@Client.on_callback_query(custom_filters.get_users_filter & custom_filters.check_user_filter & custom_filters.user_is_administrator)
@inject_user
async def get_users_callback(client: Client, callback_query: CallbackQuery, user: User) -> None:
    users = [
        [
            InlineKeyboardButton(
                Translator.translate(Strings.UserBtn, user.locale, user_id=i.user_id),
                f"user_info#{i.user_id}"
            )
        ]
        for i in Configs.config.users
    ]

    await callback_query.edit_message_text(
        Translator.translate(Strings.AuthorizedUsers, user.locale),
        reply_markup=InlineKeyboardMarkup(
            users +
            [
                [
                    InlineKeyboardButton(Translator.translate(Strings.BackToSettings, user.locale), "settings")
                ]
            ]
        )
    )


@Client.on_callback_query(custom_filters.user_info_filter & custom_filters.check_user_filter & custom_filters.user_is_administrator)
@inject_user
async def get_user_info_callback(client: Client, callback_query: CallbackQuery, user: User) -> None:
    user_id = int(callback_query.data.split("#")[1])

    user_info = get_user_from_config(user_id)

    write_support("None", callback_query.from_user.id)

    # get all fields of the model dynamically
    fields = [
        [
            InlineKeyboardButton(
                Translator.translate(Strings.EditClientSetting, user.locale, setting=key.replace('_', ' ').capitalize()),
                f"edit_user#{user_id}-{key}-{item.annotation}"
            )
        ]
        for key, item in user_info.model_fields.items()
    ]

    confs = '\n- '.join(iter([f"**{key.capitalize()}:** {item}" for key, item in user_info.model_dump().items()]))

    await callback_query.edit_message_text(
        Translator.translate(Strings.EditUserSetting, user.locale, user_id=user_id, confs=confs),
        reply_markup=InlineKeyboardMarkup(
            fields +
            [
                [
                    InlineKeyboardButton(Translator.translate(Strings.BackToUsers, user.locale), "get_users")
                ]
            ]
        )
    )


@Client.on_callback_query(custom_filters.edit_user_filter & custom_filters.check_user_filter & custom_filters.user_is_administrator)
@inject_user
async def edit_user_callback(client: Client, callback_query: CallbackQuery, user: User) -> None:
    data = callback_query.data.split("#")[1]
    user_id = int(data.split("-")[0])
    field_to_edit = data.split("-")[1]
    data_type = convert_type_from_string(data.split("-")[2])

    user_info = get_user_from_config(user_id)

    # if field_to_edit == nameof(user.locale):
    #     pass

    if data_type == bool:
        notify_status = Translator.translate(Strings.Enabled if user_info.notify else Strings.Disabled, user.locale)

        await callback_query.edit_message_text(
            Translator.translate(Strings.EditUserField, user.locale, user_id=user_id, field_to_edit=field_to_edit),
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            notify_status,
                            f"toggle_user_var#{user_id}-{field_to_edit}")
                    ],
                    [
                        InlineKeyboardButton(
                            Translator.translate(Strings.BackToUSer, user.locale, user_id=user_id),
                            f"user_info#{user_id}"
                        )
                    ]
                ]
            )
        )

        return

    write_support(callback_query.data, callback_query.from_user.id)

    await callback_query.edit_message_text(
        Translator.translate(Strings.NewValueForUserField, user.locale, field_to_edit=field_to_edit, user_id=user_id, data_type=data_type),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        Translator.translate(Strings.BackToUSer, user.locale, user_id=user_id),
                        f"user_info#{user_id}"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(custom_filters.toggle_user_var_filter & custom_filters.check_user_filter & custom_filters.user_is_administrator)
@inject_user
async def toggle_user_var(client: Client, callback_query: CallbackQuery, user: User) -> None:
    data = callback_query.data.split("#")[1]
    user_id = int(data.split("-")[0])
    field_to_edit = data.split("-")[1]

    user_from_configs = Configs.config.users.index(user)

    if user_from_configs == -1:
        return

    Configs.config.users[user_from_configs].notify = not Configs.config.users[user_from_configs].notify
    Configs.update_config(Configs.config)

    notify_status = Translator.translate(Strings.Enabled if user.notify else Strings.Disabled, user.locale)

    await callback_query.edit_message_text(
        Translator.translate(Strings.EditUserField, user.locale, field_to_edit=field_to_edit, user_id=user_id),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        notify_status,
                        f"toggle_user_var#{user_id}-{field_to_edit}")
                ],
                [
                    InlineKeyboardButton(
                        Translator.translate(Strings.BackToUSer, user.locale, user_id=user_id),
                        f"user_info#{user_id}"
                    )
                ]
            ]
        )
    )
