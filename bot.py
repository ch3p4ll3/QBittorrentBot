import os
import tempfile

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from pyrogram.errors.exceptions import MessageIdInvalid
from pyrogram.enums.parse_mode import ParseMode
import psutil

import custom_filters
import qbittorrent_control
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from utils import torrent_finished, convert_size, convert_eta
from config import API_ID, API_HASH, TG_TOKEN, AUTHORIZED_IDS
import db_management


app = Client("qbittorrent_bot", api_id=API_ID, api_hash=API_HASH, bot_token=TG_TOKEN, parse_mode=ParseMode.MARKDOWN)

scheduler = AsyncIOScheduler()
scheduler.add_job(torrent_finished, "interval", args=[app], seconds=10)


def send_menu(message, chat) -> None:
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
        app.edit_message_text(chat, message, text="Qbittorrent Control", reply_markup=InlineKeyboardMarkup(buttons))

    except MessageIdInvalid:
        app.send_message(chat, text="Qbittorrent Control", reply_markup=InlineKeyboardMarkup(buttons))


def list_active_torrents(n, chat, message, callback, status_filter: str = None) -> None:
    torrents = qbittorrent_control.get_torrent_info(status_filter=status_filter)

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
            app.edit_message_text(chat, message, "There are no torrents", reply_markup=InlineKeyboardMarkup(buttons))
        except MessageIdInvalid:
            app.send_message(chat, "There are no torrents", reply_markup=InlineKeyboardMarkup(buttons))
        return

    buttons = [categories_buttons]

    if n == 1:
        for key, i in enumerate(torrents):
            buttons.append([InlineKeyboardButton(i.name, f"{callback}#{key+1}")])

        buttons.append([InlineKeyboardButton("🔙 Menu", "menu")])

        try:
            app.edit_message_reply_markup(chat, message, reply_markup=InlineKeyboardMarkup(buttons))
        except MessageIdInvalid:
            app.send_message(chat, "Qbittorrent Control", reply_markup=InlineKeyboardMarkup(buttons))

    else:
        for key, i in enumerate(torrents):
            buttons.append([InlineKeyboardButton(i.name, f"torrentInfo#{key+1}")])

        buttons.append([InlineKeyboardButton("🔙 Menu", "menu")])

        try:
            app.edit_message_reply_markup(chat, message, reply_markup=InlineKeyboardMarkup(buttons))
        except MessageIdInvalid:
            app.send_message(chat, "Qbittorrent Control", reply_markup=InlineKeyboardMarkup(buttons))


@app.on_message(filters=filters.command("start"))
def start_command(client: Client, message: Message) -> None:
    """Start the bot."""
    if message.from_user.id in AUTHORIZED_IDS:
        send_menu(message.id, message.chat.id)

    else:
        button = InlineKeyboardMarkup([[InlineKeyboardButton("Github",
                                                             url="https://github.com/ch3p4ll3/QBittorrentBot/")]])
        app.send_message(message.chat.id, "You are not authorized to use this bot", reply_markup=button)


@app.on_message(filters=filters.command("stats"))
def stats_command(client: Client, message: Message) -> None:
    if message.from_user.id in AUTHORIZED_IDS:

        txt = f"**============SYSTEM============**\n" \
              f"**CPU Usage:** {psutil.cpu_percent(interval=None)}%\n" \
              f"**CPU Temp:** {psutil.sensors_temperatures()['coretemp'][0].current}°C\n" \
              f"**Free Memory:** {convert_size(psutil.virtual_memory().available)} of " \
              f"{convert_size(psutil.virtual_memory().total)} ({psutil.virtual_memory().percent}%)\n" \
              f"**Disks usage:** {convert_size(psutil.disk_usage('/mnt').used)} of " \
              f"{convert_size(psutil.disk_usage('/mnt').total)} ({psutil.disk_usage('/mnt').percent}%)"

        message.reply_text(txt)

    else:
        button = InlineKeyboardMarkup([[InlineKeyboardButton("Github",
                                                             url="https://github.com/ch3p4ll3/QBittorrentBot/")]])
        app.send_message(message.chat.id, "You are not authorized to use this bot", reply_markup=button)


@app.on_callback_query(filters=custom_filters.add_category_filter)
def add_category_callback(client: Client, callback_query: CallbackQuery) -> None:
    db_management.write_support("category_name", callback_query.from_user.id)
    button = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Menu", "menu")]])
    try:
        app.edit_message_text(callback_query.from_user.id, callback_query.message.id,
                              "Send the category name", reply_markup=button)
    except MessageIdInvalid:
        app.send_message(callback_query.from_user.id, "Send the category name", reply_markup=button)


@app.on_callback_query(filters=custom_filters.select_category_filter)
def list_categories(client: Client, callback_query: CallbackQuery):
    buttons = []
    categories = qbittorrent_control.get_categories()

    if categories is None:
        buttons.append([InlineKeyboardButton("🔙 Menu", "menu")])
        app.edit_message_text(callback_query.from_user.id, callback_query.message.id,
                              "There are no categories", reply_markup=InlineKeyboardMarkup(buttons))
        return

    for key, i in enumerate(categories):
        buttons.append([InlineKeyboardButton(i, f"{callback_query.data.split('#')[1]}#{i}")])

    buttons.append([InlineKeyboardButton("🔙 Menu", "menu")])

    try:
        app.edit_message_text(callback_query.from_user.id, callback_query.message.id,
                              "Choose a category:", reply_markup=InlineKeyboardMarkup(buttons))
    except MessageIdInvalid:
        app.send_message(callback_query.from_user.id, "Choose a category:", reply_markup=InlineKeyboardMarkup(buttons))


@app.on_callback_query(filters=custom_filters.remove_category_filter)
def remove_category_callback(client: Client, callback_query: CallbackQuery) -> None:
    buttons = [[InlineKeyboardButton("🔙 Menu", "menu")]]

    qbittorrent_control.remove_category(data=callback_query.data.split("#")[1])
    app.edit_message_text(callback_query.from_user.id, callback_query.message.id,
                          f"The category {callback_query.data.split('#')[1]} has been removed",
                          reply_markup=InlineKeyboardMarkup(buttons))


@app.on_callback_query(filters=custom_filters.modify_category_filter)
def modify_category_callback(client: Client, callback_query: CallbackQuery) -> None:
    buttons = [[InlineKeyboardButton("🔙 Menu", "menu")]]

    db_management.write_support(f"category_dir_modify#{callback_query.data.split('#')[1]}", callback_query.from_user.id)
    app.edit_message_text(callback_query.from_user.id, callback_query.message.id,
                          f"Send new path for category {callback_query.data.split('#')[1]}",
                          reply_markup=InlineKeyboardMarkup(buttons))


@app.on_callback_query(filters=custom_filters.category_filter)
def category(client: Client, callback_query: CallbackQuery) -> None:
    buttons = []

    categories = qbittorrent_control.get_categories()

    if categories is None:
        if "magnet" in callback_query.data:
            addmagnet_callback(client, callback_query)

        else:
            addtorrent_callback(client, callback_query)

        return

    for key, i in enumerate(categories):
        buttons.append([InlineKeyboardButton(i, f"{callback_query.data.split('#')[1]}#{i}")])

    buttons.append([InlineKeyboardButton("None", f"{callback_query.data.split('#')[1]}#None")])
    buttons.append([InlineKeyboardButton("🔙 Menu", "menu")])

    try:
        app.edit_message_text(callback_query.from_user.id, callback_query.message.id,
                              "Choose a category:", reply_markup=InlineKeyboardMarkup(buttons))
    except MessageIdInvalid:
        app.send_message(callback_query.from_user.id, "Choose a category:", reply_markup=InlineKeyboardMarkup(buttons))


@app.on_callback_query(filters=custom_filters.menu_filter)
def menu_callback(client: Client, callback_query: CallbackQuery) -> None:
    send_menu(callback_query.message.id, callback_query.from_user.id)


@app.on_callback_query(filters=custom_filters.list_filter)
def list_callback(client: Client, callback_query: CallbackQuery) -> None:
    list_active_torrents(0, callback_query.from_user.id, callback_query.message.id,
                         db_management.read_support(callback_query.from_user.id))


@app.on_callback_query(filters=custom_filters.list_by_status_filter)
def list_by_status_callback(client: Client, callback_query: CallbackQuery) -> None:
    status_filter = callback_query.data.split("#")[1]
    list_active_torrents(0, callback_query.from_user.id, callback_query.message.id,
                         db_management.read_support(callback_query.from_user.id), status_filter=status_filter)

@app.on_callback_query(filters=custom_filters.add_magnet_filter)
def addmagnet_callback(client: Client, callback_query: CallbackQuery) -> None:
    db_management.write_support(f"magnet#{callback_query.data.split('#')[1]}", callback_query.from_user.id)
    app.answer_callback_query(callback_query.id, "Send a magnet link")


@app.on_callback_query(filters=custom_filters.add_torrent_filter)
def addtorrent_callback(client: Client, callback_query: CallbackQuery) -> None:
    db_management.write_support(f"torrent#{callback_query.data.split('#')[1]}", callback_query.from_user.id)
    app.answer_callback_query(callback_query.id, "Send a torrent file")


@app.on_callback_query(filters=custom_filters.pause_all_filter)
def pauseall_callback(client: Client, callback_query: CallbackQuery) -> None:
    qbittorrent_control.pause_all()
    app.answer_callback_query(callback_query.id, "Paused all torrents")


@app.on_callback_query(filters=custom_filters.resume_all_filter)
def resumeall_callback(client: Client, callback_query: CallbackQuery) -> None:
    qbittorrent_control.resume_all()
    app.answer_callback_query(callback_query.id, "Resumed all torrents")


@app.on_callback_query(filters=custom_filters.pause_filter)
def pause_callback(client: Client, callback_query: CallbackQuery) -> None:
    if callback_query.data.find("#") == -1:
        list_active_torrents(1, callback_query.from_user.id, callback_query.message.id, "pause")

    else:
        qbittorrent_control.pause(id_torrent=int(callback_query.data.split("#")[1]))
        send_menu(callback_query.message.id, callback_query.from_user.id)


@app.on_callback_query(filters=custom_filters.resume_filter)
def resume_callback(client: Client, callback_query: CallbackQuery) -> None:
    if callback_query.data.find("#") == -1:
        list_active_torrents(1, callback_query.from_user.id, callback_query.message.id, "resume")

    else:
        qbittorrent_control.resume(id_torrent=int(callback_query.data.split("#")[1]))
        send_menu(callback_query.message.id, callback_query.from_user.id)


@app.on_callback_query(filters=custom_filters.delete_one_filter)
def delete_callback(client: Client, callback_query: CallbackQuery) -> None:
    if callback_query.data.find("#") == -1:
        list_active_torrents(1, callback_query.from_user.id, callback_query.message.id, "delete_one")

    else:

        buttons = [[InlineKeyboardButton("🗑 Delete torrent", f"delete_one_no_data#{callback_query.data.split('#')[1]}")],
                   [InlineKeyboardButton("🗑 Delete torrent and data", f"delete_one_data#{callback_query.data.split('#')[1]}")],
                   [InlineKeyboardButton("🔙 Menu", "menu")]]

        app.edit_message_reply_markup(callback_query.from_user.id, callback_query.message.id,
                                      reply_markup=InlineKeyboardMarkup(buttons))


@app.on_callback_query(filters=custom_filters.delete_one_no_data_filter)
def delete_no_data_callback(client: Client, callback_query: CallbackQuery) -> None:
    if callback_query.data.find("#") == -1:
        list_active_torrents(1, callback_query.from_user.id, callback_query.message.id, "delete_one_no_data")

    else:
        qbittorrent_control.delete_one_no_data(id_torrent=int(callback_query.data.split("#")[1]))
        send_menu(callback_query.message.id, callback_query.from_user.id)


@app.on_callback_query(filters=custom_filters.delete_one_data_filter)
def delete_with_data_callback(client: Client, callback_query: CallbackQuery) -> None:
    if callback_query.data.find("#") == -1:
        list_active_torrents(1, callback_query.from_user.id, callback_query.message.id, "delete_one_data")

    else:
        qbittorrent_control.delete_one_data(id_torrent=int(callback_query.data.split("#")[1]))
        send_menu(callback_query.message.id, callback_query.from_user.id)


@app.on_callback_query(filters=custom_filters.delete_all_filter)
def delete_all_callback(client: Client, callback_query: CallbackQuery) -> None:
    buttons = [[InlineKeyboardButton("🗑 Delete all torrents", "delete_all_no_data")],
               [InlineKeyboardButton("🗑 Delete all torrents and data", "delete_all_data")],
               [InlineKeyboardButton("🔙 Menu", "menu")]]
    app.edit_message_reply_markup(callback_query.from_user.id, callback_query.message.id,
                                  reply_markup=InlineKeyboardMarkup(buttons))


@app.on_callback_query(filters=custom_filters.delete_all_no_data_filter)
def delete_all_with_no_data_callback(client: Client, callback_query: CallbackQuery) -> None:
    qbittorrent_control.delall_no_data()
    app.answer_callback_query(callback_query.id, "Deleted only torrents")
    send_menu(callback_query.message.id, callback_query.from_user.id)


@app.on_callback_query(filters=custom_filters.delete_all_data_filter)
def delete_all_with_data_callback(client: Client, callback_query: CallbackQuery) -> None:
    qbittorrent_control.delall_data()
    app.answer_callback_query(callback_query.id, "Deleted All+Torrents")
    send_menu(callback_query.message.id, callback_query.from_user.id)


@app.on_callback_query(filters=custom_filters.torrentInfo_filter)
def torrent_info_callback(client: Client, callback_query: CallbackQuery) -> None:
    torrent = qbittorrent_control.get_torrent_info(data=int(callback_query.data.split("#")[1]))
    progress = torrent.progress * 100
    text = ""

    if progress == 0:
        text += f"{torrent.name}\n[            ] " \
                f"{round(progress, 2)}% completed\n" \
                f"State: {torrent.state.capitalize()}\n" \
                f"Download Speed: {convert_size(torrent.dlspeed)}/s\n" \
                f"Size: {convert_size(torrent.size)}\nETA: " \
                f"{convert_eta(int(torrent.eta))}\n" \
                f"Category: {torrent.category}\n"

    elif progress == 100:
        text += f"{torrent.name}\n[completed] " \
                f"{round(progress, 2)}% completed\n" \
                f"State: {torrent.state.capitalize()}\n" \
                f"Upload Speed: {convert_size(torrent.upspeed)}/s\n" \
                f"Category: {torrent.category}\n"

    else:
        text += f"{torrent.name}\n[{'=' * int(progress / 10)}" \
                f"{' ' * int(12 - (progress / 10))}]" \
                f" {round(progress, 2)}% completed\n" \
                f"State: {torrent.state.capitalize()} \n" \
                f"Download Speed: {convert_size(torrent.dlspeed)}/s\n" \
                f"Size: {convert_size(torrent.size)}\nETA: " \
                f"{convert_eta(int(torrent.eta))}\n" \
                f"Category: {torrent.category}\n"

    buttons = [[InlineKeyboardButton("⏸ Pause", f"pause#{callback_query.data.split('#')[1]}")],
               [InlineKeyboardButton("▶️ Resume", f"resume#{callback_query.data.split('#')[1]}")],
               [InlineKeyboardButton("🗑 Delete", f"delete_one#{callback_query.data.split('#')[1]}")],
               [InlineKeyboardButton("🔙 Menu", "menu")]]

    app.edit_message_text(callback_query.from_user.id, callback_query.message.id, text=text,
                          reply_markup=InlineKeyboardMarkup(buttons))


@app.on_message()
def on_text(client: Client, message: Message) -> None:
    action = db_management.read_support(message.from_user.id)

    if "magnet" in action:
        if message.text.startswith("magnet:?xt"):
            magnet_link = message.text.split("\n")
            category = db_management.read_support(message.from_user.id).split("#")[1]
            qbittorrent_control.add_magnet(magnet_link=magnet_link,
                                           category=category)
            send_menu(message.id, message.from_user.id)
            db_management.write_support("None", message.from_user.id)

        else:
            message.reply_text("This magnet link is invalid! Retry")

    elif "torrent" in action and message.document:
        if ".torrent" in message.document.file_name:
            with tempfile.TemporaryDirectory() as tempdir:
                name = f"{tempdir}/{message.document.file_name}"
                category = db_management.read_support(message.from_user.id).split("#")[1]
                message.download(name)
                qbittorrent_control.add_torrent(file_name=name,
                                                category=category)
            send_menu(message.id, message.from_user.id)
            db_management.write_support("None", message.from_user.id)

        else:
            message.reply_text("This is not a torrent file! Retry")

    elif action == "category_name":
        db_management.write_support(f"category_dir#{message.text}", message.from_user.id)
        message.reply_text(f"now send me the path for the category {message.text}")

    elif "category_dir" in action:
        if os.path.exists(message.text):
            name = db_management.read_support(message.from_user.id).split("#")[1]

            if "modify" in action:
                qbittorrent_control.edit_category(name=name,
                                                  save_path=message.text)
                send_menu(message.id, message.from_user.id)
                return

            qbittorrent_control.create_category(name=name,
                                                save_path=message.text)
            send_menu(message.id, message.from_user.id)

        else:
            message.reply_text("The path entered does not exist! Retry")
