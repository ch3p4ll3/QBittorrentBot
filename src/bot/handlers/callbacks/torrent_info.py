#from tqdm import tqdm

from aiogram import Bot, Router
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import BufferedInputFile, CallbackQuery

from src.client_manager.client_repo import ClientRepo
from src.settings import Settings
from src.settings.user import User
from src.translator import Translator, Strings
from src.utils import convert_size, convert_eta, format_progress

from src.bot.filters.callbacks import TorrentInfo, Export, Pause, Resume, DeleteOne, Menu


def get_router():
    router = Router()

    @router.callback_query(TorrentInfo.filter())
    async def torrent_info_callback(callback_query: CallbackQuery, callback_data: TorrentInfo, settings: Settings, bot: Bot, user: User) -> None:
        repository_class = ClientRepo.get_client_manager(settings.client.type)
        torrent = await repository_class(settings).get_torrent(callback_data.torrent_hash)

        text_to_send = f"{torrent.name}\n"

        if torrent.progress == 1:
            text_to_send += Translator.translate(Strings.TorrentCompleted, user.locale)

        else:
            text_to_send += format_progress(torrent.progress)

        if "stalled" not in torrent.state:
            text_to_send += Translator.translate(
                Strings.TorrentState,
                user.locale,
                current_state=torrent.state.capitalize(),
                download_speed=convert_size(torrent.dlspeed)
            )

        text_to_send += Translator.translate(
            Strings.TorrentSize,
            user.locale,
            torrent_size=convert_size(torrent.size)
        )

        if "stalled" not in torrent.state:
            text_to_send += Translator.translate(
                Strings.TorrentEta,
                user.locale,
                torrent_eta=convert_eta(int(torrent.eta))
            )

        if torrent.category:
            text_to_send += Translator.translate(
                Strings.TorrentCategory,
                user.locale,
                torrent_category=torrent.category
            )

        buttons = [
            [
                InlineKeyboardButton( 
                    text=Translator.translate(Strings.ExportTorrentBtn, user.locale),
                    callback_data=Export(torrent_hash=callback_data.torrent_hash).pack()
                )
            ],
            [
                InlineKeyboardButton(
                    text=Translator.translate(Strings.PauseTorrentBtn, user.locale),
                    callback_data=Pause(torrent_hash=callback_data.torrent_hash).pack()
                )
            ],
            [
                InlineKeyboardButton(
                    text=Translator.translate(Strings.ResumeTorrentBtn, user.locale),
                    callback_data=Resume(torrent_hash=callback_data.torrent_hash).pack()
                )
            ],
            [
                InlineKeyboardButton(
                    text=Translator.translate(Strings.DeleteTorrentBtn, user.locale),
                    callback_data=DeleteOne(torrent_hash=callback_data.torrent_hash).pack()
                )
            ],
            [
                InlineKeyboardButton(
                    text=Translator.translate(Strings.BackToMenu, user.locale),
                    callback_data=Menu().pack()
                )
            ]
        ]

        await bot.edit_message_text(
            chat_id=callback_query.from_user.id,
            message_id=callback_query.message.message_id,
            text=text_to_send,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
        )


    @router.callback_query(Export.filter())
    async def export_callback(callback_query: CallbackQuery, callback_data: Export, settings: Settings, bot: Bot) -> None:
        repository_class = ClientRepo.get_client_manager(settings.client.type)
        file_bytes = await repository_class(settings).export_torrent(callback_data.torrent_hash)

        await bot.send_document(
            callback_query.from_user.id,
            BufferedInputFile(file_bytes.read(), file_bytes.name)
        )

    return router
