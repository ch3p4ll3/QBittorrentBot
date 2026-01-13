from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
import psutil

from .. import custom_filters
from ...db_management import write_support
from ...utils import convert_size, inject_user
from .common import send_menu
from ...settings.user import User
from ...translator import Translator, Strings


@Client.on_message(~custom_filters.check_user_filter)
async def access_denied_message(client: Client, message: Message) -> None:
    button = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "Github",
                    url="https://github.com/ch3p4ll3/QBittorrentBot/"
                )
            ]
        ]
    )

    await client.send_message(message.chat.id, "You are not authorized to use this bot", reply_markup=button)


@Client.on_message(filters.command("start") & custom_filters.check_user_filter)
async def start_command(client: Client, message: Message) -> None:
    """Start the bot."""
    write_support("None", message.chat.id)
    await send_menu(client, message.id, message.chat.id)


@Client.on_message(filters.command("stats") & custom_filters.check_user_filter)
@inject_user
async def stats_command(client: Client, message: Message, user: User) -> None:
    stats_text = Translator.translate(
        Strings.StatsCommand,
        user.locale,
        cpu_usage=psutil.cpu_percent(interval=None),
        cpu_temp=psutil.sensors_temperatures()['coretemp'][0].current,
        free_memory=convert_size(psutil.virtual_memory().available),
        total_memory=convert_size(psutil.virtual_memory().total),
        memory_percent=psutil.virtual_memory().percent,
        disk_used=convert_size(psutil.disk_usage('/mnt').used),
        disk_total=convert_size(psutil.disk_usage('/mnt').total),
        disk_percent=psutil.disk_usage('/mnt').percent
    )

    await client.send_message(message.chat.id, stats_text)
