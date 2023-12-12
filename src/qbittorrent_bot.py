import os
import tempfile

from tqdm import tqdm

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from pyrogram.errors.exceptions import MessageIdInvalid
from pyrogram.enums.parse_mode import ParseMode
import psutil

from src import custom_filters
from src.qbittorrent_manager import QbittorrentManagement
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from src.utils import torrent_finished, convert_size, convert_eta
from src.config import BOT_CONFIGS
from src import db_management

app = Client(
    "qbittorrent_bot",
    api_id=BOT_CONFIGS.telegram.api_id,
    api_hash=BOT_CONFIGS.telegram.api_hash,
    bot_token=BOT_CONFIGS.telegram.bot_token,
    parse_mode=ParseMode.MARKDOWN
)

scheduler = AsyncIOScheduler()
scheduler.add_job(torrent_finished, "interval", args=[app], seconds=60)


async def send_menu(client: Client, message, chat) -> None:
    db_management.write_support("None", chat)
    buttons = [[InlineKeyboardButton("📝 List", "list")],
               [InlineKeyboardButton("➕ Add Magnet", "category#add_magnet"),
                InlineKeyboardButton("➕ Add Torrent", "category#add_torrent")],
               [InlineKeyboardButton("⏸ Pause", "pause"),
                InlineKeyboardButton("▶️ Resume", "resume")],
               [InlineKeyboardButton("⏸ Pause All", "pause_all"),
                InlineKeyboardButton("▶️ Resume All", "resume_all")],
               [InlineKeyboardButton("🗑 Delete", "delete_one"),
                InlineKeyboardButton("🗑 Delete All", "delete_all")],
               [InlineKeyboardButton("➕ Add Category", "add_category"),
                InlineKeyboardButton("🗑 Remove Category", "select_category#remove_category")],
               [InlineKeyboardButton("📝 Modify Category", "select_category#modify_category")]]

    try:
        await client.edit_message_text(chat, message, text="Qbittorrent Control",
                                       reply_markup=InlineKeyboardMarkup(buttons))

    except MessageIdInvalid:
        await client.send_message(chat, text="Qbittorrent Control", reply_markup=InlineKeyboardMarkup(buttons))


async def list_active_torrents(client: Client, n, chat, message, callback, status_filter: str = None) -> None:
    with QbittorrentManagement() as qb:
        torrents = qb.get_torrent_info(status_filter=status_filter)

    def render_categories_buttons():
        return [
            InlineKeyboardButton(f"⏳ {'*' if status_filter == 'downloading' else ''} Downloading",
                                 "by_status_list#downloading"),
            InlineKeyboardButton(f"✔️ {'*' if status_filter == 'completed' else ''} Completed",
                                 "by_status_list#completed"),
            InlineKeyboardButton(f"⏸️ {'*' if status_filter == 'paused' else ''} Paused", "by_status_list#paused"),
        ]

    categories_buttons = render_categories_buttons()
    if not torrents:
        buttons = [categories_buttons, [InlineKeyboardButton("🔙 Menu", "menu")]]
        try:
            await client.edit_message_text(chat, message, "There are no torrents",
                                           reply_markup=InlineKeyboardMarkup(buttons))
        except MessageIdInvalid:
            await client.send_message(chat, "There are no torrents", reply_markup=InlineKeyboardMarkup(buttons))
        return

    buttons = [categories_buttons]

    if n == 1:
        for key, i in enumerate(torrents):
            buttons.append([InlineKeyboardButton(i.name, f"{callback}#{i.info.hash}")])

        buttons.append([InlineKeyboardButton("🔙 Menu", "menu")])

        try:
            await client.edit_message_reply_markup(chat, message, reply_markup=InlineKeyboardMarkup(buttons))
        except MessageIdInvalid:
            await client.send_message(chat, "Qbittorrent Control", reply_markup=InlineKeyboardMarkup(buttons))

    else:
        for key, i in enumerate(torrents):
            buttons.append([InlineKeyboardButton(i.name, f"torrentInfo#{i.info.hash}")])

        buttons.append([InlineKeyboardButton("🔙 Menu", "menu")])

        try:
            await client.edit_message_reply_markup(chat, message, reply_markup=InlineKeyboardMarkup(buttons))
        except MessageIdInvalid:
            await client.send_message(chat, "Qbittorrent Control", reply_markup=InlineKeyboardMarkup(buttons))


@app.on_message(filters=filters.command("start"))
async def start_command(client: Client, message: Message) -> None:
    """Start the bot."""
    if message.from_user.id in [i.user_id for i in BOT_CONFIGS.users]:
        await send_menu(client, message.id, message.chat.id)

    else:
        button = InlineKeyboardMarkup([[InlineKeyboardButton("Github",
                                                             url="https://github.com/ch3p4ll3/QBittorrentBot/")]])
        await client.send_message(message.chat.id, "You are not authorized to use this bot", reply_markup=button)


@app.on_message(filters=filters.command("stats"))
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


@app.on_callback_query(filters=custom_filters.add_category_filter)
async def add_category_callback(client: Client, callback_query: CallbackQuery) -> None:
    db_management.write_support("category_name", callback_query.from_user.id)
    button = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Menu", "menu")]])
    try:
        await client.edit_message_text(callback_query.from_user.id, callback_query.message.id,
                                       "Send the category name", reply_markup=button)
    except MessageIdInvalid:
        await client.send_message(callback_query.from_user.id, "Send the category name", reply_markup=button)


@app.on_callback_query(filters=custom_filters.select_category_filter)
async def list_categories(client: Client, callback_query: CallbackQuery):
    buttons = []

    with QbittorrentManagement() as qb:
        categories = qb.get_categories()

    if categories is None:
        buttons.append([InlineKeyboardButton("🔙 Menu", "menu")])
        await client.edit_message_text(callback_query.from_user.id, callback_query.message.id,
                                       "There are no categories", reply_markup=InlineKeyboardMarkup(buttons))
        return

    for key, i in enumerate(categories):
        buttons.append([InlineKeyboardButton(i, f"{callback_query.data.split('#')[1]}#{i}")])

    buttons.append([InlineKeyboardButton("🔙 Menu", "menu")])

    try:
        await client.edit_message_text(callback_query.from_user.id, callback_query.message.id,
                                       "Choose a category:", reply_markup=InlineKeyboardMarkup(buttons))
    except MessageIdInvalid:
        await client.send_message(callback_query.from_user.id, "Choose a category:",
                                  reply_markup=InlineKeyboardMarkup(buttons))


@app.on_callback_query(filters=custom_filters.remove_category_filter)
async def remove_category_callback(client: Client, callback_query: CallbackQuery) -> None:
    buttons = [[InlineKeyboardButton("🔙 Menu", "menu")]]

    with QbittorrentManagement() as qb:
        qb.remove_category(data=callback_query.data.split("#")[1])

    await client.edit_message_text(callback_query.from_user.id, callback_query.message.id,
                                   f"The category {callback_query.data.split('#')[1]} has been removed",
                                   reply_markup=InlineKeyboardMarkup(buttons))


@app.on_callback_query(filters=custom_filters.modify_category_filter)
async def modify_category_callback(client: Client, callback_query: CallbackQuery) -> None:
    buttons = [[InlineKeyboardButton("🔙 Menu", "menu")]]

    db_management.write_support(f"category_dir_modify#{callback_query.data.split('#')[1]}", callback_query.from_user.id)
    await client.edit_message_text(callback_query.from_user.id, callback_query.message.id,
                                   f"Send new path for category {callback_query.data.split('#')[1]}",
                                   reply_markup=InlineKeyboardMarkup(buttons))


@app.on_callback_query(filters=custom_filters.category_filter)
async def category(client: Client, callback_query: CallbackQuery) -> None:
    buttons = []

    with QbittorrentManagement() as qb:
        categories = qb.get_categories()

    if categories is None:
        if "magnet" in callback_query.data:
            await add_magnet_callback(client, callback_query)

        else:
            await add_torrent_callback(client, callback_query)

        return

    for key, i in enumerate(categories):
        buttons.append([InlineKeyboardButton(i, f"{callback_query.data.split('#')[1]}#{i}")])

    buttons.append([InlineKeyboardButton("None", f"{callback_query.data.split('#')[1]}#None")])
    buttons.append([InlineKeyboardButton("🔙 Menu", "menu")])

    try:
        await client.edit_message_text(callback_query.from_user.id, callback_query.message.id,
                                       "Choose a category:", reply_markup=InlineKeyboardMarkup(buttons))
    except MessageIdInvalid:
        await client.send_message(callback_query.from_user.id, "Choose a category:",
                                  reply_markup=InlineKeyboardMarkup(buttons))


@app.on_callback_query(filters=custom_filters.menu_filter)
async def menu_callback(client: Client, callback_query: CallbackQuery) -> None:
    await send_menu(client, callback_query.message.id, callback_query.from_user.id)


@app.on_callback_query(filters=custom_filters.list_filter)
async def list_callback(client: Client, callback_query: CallbackQuery) -> None:
    await list_active_torrents(client, 0, callback_query.from_user.id, callback_query.message.id,
                               db_management.read_support(callback_query.from_user.id))


@app.on_callback_query(filters=custom_filters.list_by_status_filter)
async def list_by_status_callback(client: Client, callback_query: CallbackQuery) -> None:
    status_filter = callback_query.data.split("#")[1]
    await list_active_torrents(client,0, callback_query.from_user.id, callback_query.message.id,
                               db_management.read_support(callback_query.from_user.id), status_filter=status_filter)


@app.on_callback_query(filters=custom_filters.add_magnet_filter)
async def add_magnet_callback(client: Client, callback_query: CallbackQuery) -> None:
    db_management.write_support(f"magnet#{callback_query.data.split('#')[1]}", callback_query.from_user.id)
    await client.answer_callback_query(callback_query.id, "Send a magnet link")


@app.on_callback_query(filters=custom_filters.add_torrent_filter)
async def add_torrent_callback(client: Client, callback_query: CallbackQuery) -> None:
    db_management.write_support(f"torrent#{callback_query.data.split('#')[1]}", callback_query.from_user.id)
    await client.answer_callback_query(callback_query.id, "Send a torrent file")


@app.on_callback_query(filters=custom_filters.pause_all_filter)
async def pause_all_callback(client: Client, callback_query: CallbackQuery) -> None:
    with QbittorrentManagement() as qb:
        qb.pause_all()
    await client.answer_callback_query(callback_query.id, "Paused all torrents")


@app.on_callback_query(filters=custom_filters.resume_all_filter)
async def resume_all_callback(client: Client, callback_query: CallbackQuery) -> None:
    with QbittorrentManagement() as qb:
        qb.resume_all()
    await client.answer_callback_query(callback_query.id, "Resumed all torrents")


@app.on_callback_query(filters=custom_filters.pause_filter)
async def pause_callback(client: Client, callback_query: CallbackQuery) -> None:
    if callback_query.data.find("#") == -1:
        await list_active_torrents(client, 1, callback_query.from_user.id, callback_query.message.id, "pause")

    else:
        with QbittorrentManagement() as qb:
            qb.pause(torrent_hash=callback_query.data.split("#")[1])
        await send_menu(client, callback_query.message.id, callback_query.from_user.id)


@app.on_callback_query(filters=custom_filters.resume_filter)
async def resume_callback(client: Client, callback_query: CallbackQuery) -> None:
    if callback_query.data.find("#") == -1:
        await list_active_torrents(client, 1, callback_query.from_user.id, callback_query.message.id, "resume")

    else:
        with QbittorrentManagement() as qb:
            qb.resume(torrent_hash=callback_query.data.split("#")[1])
        await send_menu(client, callback_query.message.id, callback_query.from_user.id)


@app.on_callback_query(filters=custom_filters.delete_one_filter)
async def delete_callback(client: Client, callback_query: CallbackQuery) -> None:
    if callback_query.data.find("#") == -1:
        await list_active_torrents(client, 1, callback_query.from_user.id, callback_query.message.id, "delete_one")

    else:

        buttons = [
            [InlineKeyboardButton("🗑 Delete torrent", f"delete_one_no_data#{callback_query.data.split('#')[1]}")],
            [InlineKeyboardButton("🗑 Delete torrent and data", f"delete_one_data#{callback_query.data.split('#')[1]}")],
            [InlineKeyboardButton("🔙 Menu", "menu")]]

        await client.edit_message_reply_markup(callback_query.from_user.id, callback_query.message.id,
                                               reply_markup=InlineKeyboardMarkup(buttons))


@app.on_callback_query(filters=custom_filters.delete_one_no_data_filter)
async def delete_no_data_callback(client: Client, callback_query: CallbackQuery) -> None:
    if callback_query.data.find("#") == -1:
        await list_active_torrents(client, 1, callback_query.from_user.id, callback_query.message.id, "delete_one_no_data")

    else:
        with QbittorrentManagement() as qb:
            qb.delete_one_no_data(torrent_hash=callback_query.data.split("#")[1])
        await send_menu(client, callback_query.message.id, callback_query.from_user.id)


@app.on_callback_query(filters=custom_filters.delete_one_data_filter)
async def delete_with_data_callback(client: Client, callback_query: CallbackQuery) -> None:
    if callback_query.data.find("#") == -1:
        await list_active_torrents(client, 1, callback_query.from_user.id, callback_query.message.id, "delete_one_data")

    else:
        with QbittorrentManagement() as qb:
            qb.delete_one_data(torrent_hash=callback_query.data.split("#")[1])
        await send_menu(client, callback_query.message.id, callback_query.from_user.id)


@app.on_callback_query(filters=custom_filters.delete_all_filter)
async def delete_all_callback(client: Client, callback_query: CallbackQuery) -> None:
    buttons = [[InlineKeyboardButton("🗑 Delete all torrents", "delete_all_no_data")],
               [InlineKeyboardButton("🗑 Delete all torrents and data", "delete_all_data")],
               [InlineKeyboardButton("🔙 Menu", "menu")]]
    await client.edit_message_reply_markup(callback_query.from_user.id, callback_query.message.id,
                                           reply_markup=InlineKeyboardMarkup(buttons))


@app.on_callback_query(filters=custom_filters.delete_all_no_data_filter)
async def delete_all_with_no_data_callback(client: Client, callback_query: CallbackQuery) -> None:
    with QbittorrentManagement() as qb:
        qb.delete_all_no_data()
    await client.answer_callback_query(callback_query.id, "Deleted only torrents")
    await send_menu(client, callback_query.message.id, callback_query.from_user.id)


@app.on_callback_query(filters=custom_filters.delete_all_data_filter)
async def delete_all_with_data_callback(client: Client, callback_query: CallbackQuery) -> None:
    with QbittorrentManagement() as qb:
        qb.delete_all_data()
    await client.answer_callback_query(callback_query.id, "Deleted All+Torrents")
    await send_menu(client, callback_query.message.id, callback_query.from_user.id)


@app.on_callback_query(filters=custom_filters.torrentInfo_filter)
async def torrent_info_callback(client: Client, callback_query: CallbackQuery) -> None:
    with QbittorrentManagement() as qb:
        torrent = qb.get_torrent_info(data=callback_query.data.split("#")[1])

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

    buttons = [[InlineKeyboardButton("⏸ Pause", f"pause#{callback_query.data.split('#')[1]}")],
               [InlineKeyboardButton("▶️ Resume", f"resume#{callback_query.data.split('#')[1]}")],
               [InlineKeyboardButton("🗑 Delete", f"delete_one#{callback_query.data.split('#')[1]}")],
               [InlineKeyboardButton("🔙 Menu", "menu")]]

    await client.edit_message_text(callback_query.from_user.id, callback_query.message.id, text=text,
                                   reply_markup=InlineKeyboardMarkup(buttons))


@app.on_message(filters=~filters.me)
async def on_text(client: Client, message: Message) -> None:
    action = db_management.read_support(message.from_user.id)

    if "magnet" in action:
        if message.text.startswith("magnet:?xt"):
            magnet_link = message.text.split("\n")
            category = db_management.read_support(message.from_user.id).split("#")[1]

            with QbittorrentManagement() as qb:
                qb.add_magnet(magnet_link=magnet_link,
                              category=category)

            await send_menu(client, message.id, message.from_user.id)
            db_management.write_support("None", message.from_user.id)

        else:
            await client.send_message(message.from_user.id, "This magnet link is invalid! Retry")

    elif "torrent" in action and message.document:
        if ".torrent" in message.document.file_name:
            with tempfile.TemporaryDirectory() as tempdir:
                name = f"{tempdir}/{message.document.file_name}"
                category = db_management.read_support(message.from_user.id).split("#")[1]
                await message.download(name)

                with QbittorrentManagement() as qb:
                    qb.add_torrent(file_name=name,
                                   category=category)
            await send_menu(client, message.id, message.from_user.id)
            db_management.write_support("None", message.from_user.id)

        else:
            await client.send_message(message.from_user.id, "This is not a torrent file! Retry")

    elif action == "category_name":
        db_management.write_support(f"category_dir#{message.text}", message.from_user.id)
        await client.send_message(message.from_user.id, f"now send me the path for the category {message.text}")

    elif "category_dir" in action:
        if os.path.exists(message.text):
            name = db_management.read_support(message.from_user.id).split("#")[1]

            if "modify" in action:
                with QbittorrentManagement() as qb:
                    qb.edit_category(name=name,
                                     save_path=message.text)
                await send_menu(client, message.id, message.from_user.id)
                return

            with QbittorrentManagement() as qb:
                qb.create_category(name=name,
                                   save_path=message.text)
            await send_menu(client, message.id, message.from_user.id)

        else:
            await client.send_message(message.from_user.id, "The path entered does not exist! Retry")

    else:
        await client.send_message(message.from_user.id, "The command does not exist")
