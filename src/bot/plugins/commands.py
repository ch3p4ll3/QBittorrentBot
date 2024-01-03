from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
import psutil

from .. import custom_filters
from ...db_management import write_support
from ...utils import convert_size
from .common import send_menu


@Client.on_message(~custom_filters.check_user_filter)
async def access_denied_message(client: Client, message: Message) -> None:
    button = InlineKeyboardMarkup([[InlineKeyboardButton("Github",
                                                         url="https://github.com/ch3p4ll3/QBittorrentBot/")]])
    await client.send_message(message.chat.id, "You are not authorized to use this bot", reply_markup=button)


@Client.on_message(filters.command("start") & custom_filters.check_user_filter)
async def start_command(client: Client, message: Message) -> None:
    """Start the bot."""
    write_support("None", message.chat.id)
    await send_menu(client, message.id, message.chat.id)


@Client.on_message(filters.command("stats") & custom_filters.check_user_filter)
async def stats_command(client: Client, message: Message) -> None:
    stats_text = f"**============SYSTEM============**\n" \
                 f"**CPU Usage:** {psutil.cpu_percent(interval=None)}%\n" \
                 f"**CPU Temp:** {psutil.sensors_temperatures()['coretemp'][0].current}°C\n" \
                 f"**Free Memory:** {convert_size(psutil.virtual_memory().available)} of " \
                 f"{convert_size(psutil.virtual_memory().total)} ({psutil.virtual_memory().percent}%)\n" \
                 f"**Disks usage:** {convert_size(psutil.disk_usage('/mnt').used)} of " \
                 f"{convert_size(psutil.disk_usage('/mnt').total)} ({psutil.disk_usage('/mnt').percent}%)"

    await client.send_message(message.chat.id, stats_text)
