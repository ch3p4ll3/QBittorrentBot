from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
import psutil

from ...utils import convert_size
from ...configs import Configs
from .common import send_menu


BOT_CONFIGS = Configs.load_config()


@Client.on_message(filters.command("start"))
async def start_command(client: Client, message: Message) -> None:
    """Start the bot."""
    if message.from_user.id in [i.user_id for i in BOT_CONFIGS.users]:
        await send_menu(client, message.id, message.chat.id)

    else:
        button = InlineKeyboardMarkup([[InlineKeyboardButton("Github",
                                                             url="https://github.com/ch3p4ll3/QBittorrentBot/")]])
        await client.send_message(message.chat.id, "You are not authorized to use this bot", reply_markup=button)


@Client.on_message(filters.command("stats"))
async def stats_command(client: Client, message: Message) -> None:
    if message.from_user.id in [i.user_id for i in BOT_CONFIGS.users]:

        stats_text = f"**============SYSTEM============**\n" \
                     f"**CPU Usage:** {psutil.cpu_percent(interval=None)}%\n" \
                     f"**CPU Temp:** {psutil.sensors_temperatures()['coretemp'][0].current}°C\n" \
                     f"**Free Memory:** {convert_size(psutil.virtual_memory().available)} of " \
                     f"{convert_size(psutil.virtual_memory().total)} ({psutil.virtual_memory().percent}%)\n" \
                     f"**Disks usage:** {convert_size(psutil.disk_usage('/mnt').used)} of " \
                     f"{convert_size(psutil.disk_usage('/mnt').total)} ({psutil.disk_usage('/mnt').percent}%)"

        await client.send_message(message.chat.id, stats_text)

    else:
        button = InlineKeyboardMarkup([[InlineKeyboardButton("Github",
                                                             url="https://github.com/ch3p4ll3/QBittorrentBot/")]])
        await client.send_message(message.chat.id, "You are not authorized to use this bot", reply_markup=button)
