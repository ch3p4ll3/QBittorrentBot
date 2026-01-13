from pyrogram import Client
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from .... import custom_filters
from .....settings import Configs
from .....settings.user import User
from .....client_manager import ClientRepo
from .....utils import convert_type_from_string, inject_user
from .....db_management import write_support
from .....translator import Translator, Strings


@Client.on_callback_query(custom_filters.edit_client_settings_filter & custom_filters.check_user_filter & custom_filters.user_is_administrator)
@inject_user
async def edit_client_settings_callback(client: Client, callback_query: CallbackQuery, user: User) -> None:
    confs = '\n- '.join(iter([f"**{key.capitalize()}:** {item}" for key, item in Configs.config.client.model_dump().items()]))

    repository = ClientRepo.get_client_manager(Configs.config.client.type)
    speed_limit = repository.get_speed_limit_mode()

    speed_limit_status = Translator.translate(Strings.Enabled if speed_limit else Strings.Disabled, user.locale)

    confs += Translator.translate(
        Strings.SpeedLimitStatus,
        user.locale,
        speed_limit_status=speed_limit_status
    )

    await callback_query.edit_message_text(
        Translator.translate(Strings.EditClientSettings, user.locale, client_type=Configs.config.client.type, configs=confs),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(Translator.translate(Strings.EditClientSettingsBtn, user.locale), "lst_client")
                ],
                [
                    InlineKeyboardButton(Translator.translate(Strings.ToggleSpeedLimit, user.locale), "toggle_speed_limit")
                ],
                [
                    InlineKeyboardButton(Translator.translate(Strings.CheckClientConnection, user.locale), "check_connection")
                ],
                [
                    InlineKeyboardButton(Translator.translate(Strings.BackToSettings, user.locale), "settings")
                ]
            ]
        )
    )


@Client.on_callback_query(custom_filters.toggle_speed_limit_filter & custom_filters.check_user_filter & custom_filters.user_is_administrator)
@inject_user
async def toggle_speed_limit_callback(client: Client, callback_query: CallbackQuery, user: User) -> None:
    confs = '\n- '.join(iter([f"**{key.capitalize()}:** {item}" for key, item in Configs.config.client.model_dump().items()]))

    repository = ClientRepo.get_client_manager(Configs.config.client.type)
    speed_limit = repository.toggle_speed_limit()

    speed_limit_status = Translator.translate(Strings.Enabled if speed_limit else Strings.Disabled, user.locale)

    confs += Translator.translate(
        Strings.SpeedLimitStatus,
        user.locale,
        speed_limit_status=speed_limit_status
    )

    await callback_query.edit_message_text(
        Translator.translate(Strings.EditClientSettings, user.locale, client_type=Configs.config.client.type, configs=confs),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(Translator.translate(Strings.EditClientSettingsBtn, user.locale), "lst_client")
                ],
                [
                    InlineKeyboardButton(Translator.translate(Strings.ToggleSpeedLimit, user.locale), "toggle_speed_limit")
                ],
                [
                    InlineKeyboardButton(Translator.translate(Strings.CheckClientConnection, user.locale), "check_connection")
                ],
                [
                    InlineKeyboardButton(Translator.translate(Strings.BackToSettings, user.locale), "settings")
                ]
            ]
        )
    )


@Client.on_callback_query(custom_filters.check_connection_filter & custom_filters.check_user_filter & custom_filters.user_is_administrator)
@inject_user
async def check_connection_callback(client: Client, callback_query: CallbackQuery, user: User) -> None:
    try:
        repository = ClientRepo.get_client_manager(Configs.config.client.type)
        version = repository.check_connection()

        await callback_query.answer(Translator.translate(Strings.ClientConnectionOk, user.locale, version=version), show_alert=True)
    except Exception:
        await callback_query.answer(Translator.translate(Strings.ClientConnectionBad, user.locale), show_alert=True)


@Client.on_callback_query(custom_filters.list_client_settings_filter & custom_filters.check_user_filter & custom_filters.user_is_administrator)
@inject_user
async def list_client_settings_callback(client: Client, callback_query: CallbackQuery, user: User) -> None:
    # get all fields of the model dynamically
    fields = [
        [
            InlineKeyboardButton(
                Translator.translate(Strings.EditClientSetting, user.locale, setting=key.replace('_', ' ').capitalize()),
                f"edit_clt#{key}-{item.annotation}"
            )
        ]
        for key, item in Configs.config.client.model_fields.items()
    ]

    await callback_query.edit_message_text(
        Translator.translate(Strings.EditClientType, user.locale, client_type=Configs.config.client.type),
        reply_markup=InlineKeyboardMarkup(
            fields +
            [
                [
                    InlineKeyboardButton(Translator.translate(Strings.BackToSettings, user.locale), "settings")
                ]
            ]
        )
    )


@Client.on_callback_query(custom_filters.edit_client_setting_filter & custom_filters.check_user_filter & custom_filters.user_is_administrator)
@inject_user
async def edit_client_setting_callback(client: Client, callback_query: CallbackQuery, user: User) -> None:
    data = callback_query.data.split("#")[1]
    field_to_edit = data.split("-")[0]
    data_type = convert_type_from_string(data.split("-")[1])

    write_support(callback_query.data, callback_query.from_user.id)

    await callback_query.edit_message_text(
        Translator.translate(Strings.NewValueForClientField, user.locale, field_to_edit=field_to_edit, data_type=data_type),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(Translator.translate(Strings.BackToSettings, user.locale), "settings")
                ]
            ]
        )
    )
