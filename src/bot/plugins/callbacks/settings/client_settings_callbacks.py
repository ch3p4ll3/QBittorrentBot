from pyrogram import Client
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from .... import custom_filters
from .....configs import Configs
from .....qbittorrent_manager import QbittorrentManagement
from .....utils import convert_type_from_string
from .....db_management import write_support


@Client.on_callback_query(custom_filters.edit_client_settings_filter & custom_filters.check_user_filter & custom_filters.user_is_administrator)
async def edit_client_settings_callback(client: Client, callback_query: CallbackQuery) -> None:
    confs = '\n- '.join(iter([f"**{key.capitalize()}:** {item}" for key, item in Configs.config.clients.model_dump().items()]))

    await callback_query.edit_message_text(
        f"Edit Qbittorrent Client Settings \n\n**Current Settings:**\n- {confs}",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("📝 Edit Client Settings", "lst_client")
                ],
                [
                    InlineKeyboardButton("✅ Check Client connection", "check_connection")
                ],
                [
                    InlineKeyboardButton("🔙 Settings", "settings")
                ]
            ]
        )
    )


@Client.on_callback_query(custom_filters.check_connection_filter)
async def check_connection_callback(client: Client, callback_query: CallbackQuery) -> None:
    try:
        with QbittorrentManagement() as qb:
            version = qb.check_connection()
            await callback_query.answer(f"✅ The connection works. QBittorrent version: {version}", show_alert=True)
    except Exception:
        await callback_query.answer("❌ Unable to establish connection with QBittorrent", show_alert=True)


@Client.on_callback_query(custom_filters.list_client_settings_filter)
async def list_client_settings_callback(client: Client, callback_query: CallbackQuery) -> None:
    # get all fields of the model dynamically
    fields = [
        [InlineKeyboardButton(f"Edit {key.replace('_', ' ').capitalize()}",
                              f"edit_clt#{key}-{item.annotation}")]
        for key, item in Configs.config.clients.model_fields.items()
    ]

    await callback_query.edit_message_text(
        f"Edit Qbittorrent Client",
        reply_markup=InlineKeyboardMarkup(
            fields +
            [
                [
                    InlineKeyboardButton("🔙 Settings", "settings")
                ]
            ]
        )
    )


@Client.on_callback_query(custom_filters.edit_client_setting_filter)
async def edit_client_setting_callback(client: Client, callback_query: CallbackQuery) -> None:
    data = callback_query.data.split("#")[1]
    field_to_edit = data.split("-")[0]
    data_type = convert_type_from_string(data.split("-")[1])

    write_support(callback_query.data, callback_query.from_user.id)

    await callback_query.edit_message_text(
        f"Send the new value for field \"{field_to_edit}\" for client. \n\n**Note:** the field type is \"{data_type}\"",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🔙 Settings", "settings")
                ]
            ]
        )
    )
