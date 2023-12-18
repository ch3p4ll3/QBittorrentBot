from tqdm import tqdm

from pyrogram import Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from ... import custom_filters
from ....client_manager import ClientRepo
from ....configs import Configs
from ....utils import convert_size, convert_eta


@Client.on_callback_query(custom_filters.torrentInfo_filter & custom_filters.check_user_filter)
async def torrent_info_callback(client: Client, callback_query: CallbackQuery) -> None:
    repository = ClientRepo.get_client_manager(Configs.config.client.type)
    torrent = repository.get_torrent_info(callback_query.data.split("#")[1])

    text = f"{torrent.name}\n"

    if torrent.progress == 1:
        text += "**COMPLETED**\n"

    else:
        text += f"{tqdm.format_meter(torrent.progress, 1, 0, bar_format='{l_bar}{bar}|')}\n"

    if "stalled" not in torrent.state:
        text += (f"**State:** {torrent.state.capitalize()} \n"
                 f"**Download Speed:** {convert_size(torrent.dlspeed)}/s\n")

    text += f"**Size:** {convert_size(torrent.size)}\n"

    if "stalled" not in torrent.state:
        text += f"**ETA:** {convert_eta(int(torrent.eta))}\n"

    if torrent.category:
        text += f"**Category:** {torrent.category}\n"

    buttons = [
        [
            InlineKeyboardButton("💾 Export torrent", f"export#{callback_query.data.split('#')[1]}")
        ],
        [
           InlineKeyboardButton("⏸ Pause", f"pause#{callback_query.data.split('#')[1]}")
        ],
        [
           InlineKeyboardButton("▶️ Resume", f"resume#{callback_query.data.split('#')[1]}")
        ],
        [
           InlineKeyboardButton("🗑 Delete", f"delete_one#{callback_query.data.split('#')[1]}")
        ],
        [
           InlineKeyboardButton("🔙 Menu", "menu")
        ]
    ]

    await client.edit_message_text(callback_query.from_user.id, callback_query.message.id, text=text,
                                   reply_markup=InlineKeyboardMarkup(buttons))


@Client.on_callback_query(custom_filters.export_filter & custom_filters.check_user_filter)
async def export_callback(client: Client, callback_query: CallbackQuery) -> None:
    repository = ClientRepo.get_client_manager(Configs.config.client.type)
    file_bytes = repository.export_torrent(torrent_hash=callback_query.data.split("#")[1])

    await client.send_document(
        callback_query.from_user.id,
        file_bytes
    )
