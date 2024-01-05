from tqdm import tqdm

from pyrogram import Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from ... import custom_filters
from ....client_manager import ClientRepo
from ....configs import Configs
from ....configs.user import User
from ....translator import Translator, Strings
from ....utils import convert_size, convert_eta, inject_user


@Client.on_callback_query(custom_filters.torrentInfo_filter & custom_filters.check_user_filter)
@inject_user
async def torrent_info_callback(client: Client, callback_query: CallbackQuery, user: User) -> None:
    repository = ClientRepo.get_client_manager(Configs.config.client.type)
    torrent = repository.get_torrent_info(callback_query.data.split("#")[1])

    text = f"{torrent.name}\n"

    if torrent.progress == 1:
        text += Translator.translate(Strings.TorrentCompleted, user.locale)

    else:
        text += f"{tqdm.format_meter(torrent.progress, 1, 0, bar_format='{l_bar}{bar}|')}\n"

    if "stalled" not in torrent.state:
        text += Translator.translate(
            Strings.TorrentState,
            user.locale,
            current_state=torrent.state.capitalize(),
            download_speed=convert_size(torrent.dlspeed)
        )

    text += Translator.translate(
        Strings.TorrentSize,
        user.locale,
        torrent_size=convert_size(torrent.size)
    )

    if "stalled" not in torrent.state:
        text += Translator.translate(
            Strings.TorrentEta,
            user.locale,
            torrent_eta=convert_eta(int(torrent.eta))
        )

    if torrent.category:
        text += Translator.translate(
            Strings.TorrentCategory,
            user.locale,
            torrent_category=torrent.category
        )

    buttons = [
        [
            InlineKeyboardButton(Translator.translate(Strings.ExportTorrentBtn, user.locale), f"export#{callback_query.data.split('#')[1]}")
        ],
        [
           InlineKeyboardButton(Translator.translate(Strings.PauseTorrentBtn, user.locale), f"pause#{callback_query.data.split('#')[1]}")
        ],
        [
           InlineKeyboardButton(Translator.translate(Strings.ResumeTorrentBtn, user.locale), f"resume#{callback_query.data.split('#')[1]}")
        ],
        [
           InlineKeyboardButton(Translator.translate(Strings.DeleteTorrentBtn, user.locale), f"delete_one#{callback_query.data.split('#')[1]}")
        ],
        [
           InlineKeyboardButton(Translator.translate(Strings.BackToMenu, user.locale), "menu")
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
