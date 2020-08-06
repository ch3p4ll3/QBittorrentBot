#!/usr/local/bin/python3.7
import datetime
import os
import tempfile
from math import log, floor

import botogram
import psutil

import qbittorrent_control
from json_validation import get_configs

bot = botogram.create(get_configs().token)
bot.about = "with this bot you can control QBittorrent from telegram"
bot.owner = "@ch3p4ll3"


@bot.prepare_memory
def prepare_memory(shared) -> None:
    shared['status'] = "None"


def convert_size(size_bytes) -> str:
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(floor(log(size_bytes, 1024)))
    p = pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


def convert_eta(n) -> str:
    return str(datetime.timedelta(seconds=n))


def send_menu(message, chat, shared) -> None:
    shared['status'] = "None"
    btn = botogram.Buttons()
    btn[0].callback("📝 List", "list")
    btn[1].callback("➕ Add Magnet", "category", "add_magnet")
    btn[1].callback("➕ Add Torrent", "category", "add_torrent")
    btn[2].callback("⏸ Pause", "pause")
    btn[2].callback("▶️ Resume", "resume")
    btn[3].callback("⏸ Pause All", "pause_all")
    btn[3].callback("▶️ Resume All", "resume_all")
    btn[4].callback("🗑 Delete", "delete_one")
    btn[4].callback("🗑 Delete All", "delete_all")
    btn[5].callback("➕ Add Category", "add_category")
    btn[5].callback("🗑 Remove Category", "remove_category")
    btn[6].callback("📝 Modify Category", "modify_category")
    try:
        message.edit("Qbitorrent Control", attach=btn)

    except Exception:
        chat.send("Qbitorrent Control", attach=btn)


def list_active_torrents(n, chat, message, callback) -> None:
    torrents = qbittorrent_control.get_torrent_info()
    if not torrents:
        btn = botogram.Buttons()
        btn[0].callback("🔙 Menu", "menu")
        try:
            message.edit("There are no torrents", attach=btn)
        except Exception:
            chat.send("There are no torrents", attach=btn)
        return

    btn = botogram.Buttons()

    if n == 1:
        for key, i in enumerate(torrents):
            btn[key].callback(i.name, callback, str(key))

        btn[key + 1].callback("🔙 Menu", "menu")

        try:
            message.edit_attach(btn)
        except Exception:
            chat.send("Qbitorrent Control", attach=btn)

    else:
        for key, i in enumerate(torrents):
            btn[key].callback(i.name, "torrentInfo", str(key))

        btn[key + 1].callback("🔙 Menu", "menu")

        try:
            message.edit_attach(btn)
        except Exception:
            chat.send("Qbitorrent Control", attach=btn)


@bot.command("start")
def start_command(message, chat, shared) -> None:
    """Start the bot."""
    if chat.id in get_configs().id:
        send_menu(message, chat, shared)

    else:
        btn = botogram.Buttons()
        btn[0].url("GitHub", "https://github.com/ch3p4ll3/QBittorrentBot/")
        chat.send("You are not authorized to use this bot.", attach=btn)


@bot.command("stats")
def stats_command(chat) -> None:
    if chat.id in get_configs().id:

        txt = f"""*============SYSTEM============*
*CPU Usage: *{psutil.cpu_percent(interval=None)}%
*CPU Temp: *{psutil.sensors_temperatures()['cpu_thermal'][0].current}°C
*Free Memory: *{convert_size(psutil.virtual_memory().available)} \
 of {convert_size(psutil.virtual_memory().total)} \
 ({psutil.virtual_memory().percent}%)
*Disks usage: *{convert_size(psutil.disk_usage('/mnt/usb').used)} \
of {convert_size(psutil.disk_usage('/mnt/usb').total)} \
({psutil.disk_usage('/mnt/usb').percent}%)"""

        chat.send(txt, syntax="markdown")

    else:
        btn = botogram.Buttons()
        btn[0].url("GitHub", "https://github.com/ch3p4ll3/QBittorrentBot/")
        chat.send("You are not authorized to use this bot.", attach=btn)


@bot.callback("add_category")
def add_category_callback(chat, message, shared) -> None:
    shared['status'] = "category_name"
    btn = botogram.Buttons()
    btn[2].callback("🔙 Menu", "menu")
    try:
        message.edit("Send the category name")
    except Exception:
        chat.send("Send the category name")


@bot.callback("remove_category")
def remove_category_callback(chat, message, data):
    btn = botogram.Buttons()

    if data is not None:
        qbittorrent_control.remove_category(data=data)
        btn[0].callback("🔙 Menu", "menu")
        message.edit(f"The category {data} has been removed", attach=btn)
        return

    categories = qbittorrent_control.get_categories()

    if categories is None:
        btn[0].callback("🔙 Menu", "menu")
        message.edit("There are no categories", attach=btn)
        return

    for key, i in enumerate(categories):
        btn[key].callback(i, "remove_category", i)

    btn[key + 1].callback("🔙 Menu", "menu")

    try:
        message.edit("Choice a category:", attach=btn)
    except Exception:
        chat.send("Choice a category:", attach=btn)


@bot.callback("modify_category")
def modify_category_callback(chat, message, data, shared):
    btn = botogram.Buttons()

    if data is not None:
        btn[2].callback("🔙 Menu", "menu")
        shared['status'] = f"category_dir_modify#{data}"
        message.edit(f"Send new path for category {data}", attach=btn)
        return

    categories = qbittorrent_control.get_categories()

    if categories is None:
        btn[0].callback("🔙 Menu", "menu")
        message.edit("There are no categories", attach=btn)
        return

    for key, i in enumerate(categories):
        btn[key].callback(i, "modify_category", i)

    btn[key + 1].callback("🔙 Menu", "menu")

    try:
        message.edit("Choice a category:", attach=btn)
    except Exception:
        chat.send("Choice a category:", attach=btn)


@bot.callback("category")
def category(chat, message, data, query, shared) -> None:
    btn = botogram.Buttons()

    categories = qbittorrent_control.get_categories()

    if categories is None:
        if "magnet" in data:
            addmagnet_callback(shared, query, "#None")

        else:
            addtorrent_callback(shared, query, "#None")

        return

    for key, i in enumerate(categories):
        btn[key].callback(i, data, i)

    btn[key + 1].callback("None", data, "None")
    btn[key + 2].callback("🔙 Menu", "menu")

    try:
        message.edit("Choice a category:", attach=btn)
    except Exception:
        chat.send("Choice a category:", attach=btn)


@bot.callback("menu")
def menu(chat, message, shared) -> None:
    send_menu(message, chat, shared)


@bot.callback("list")
def list_callback(chat, message, shared) -> None:
    btn = botogram.Buttons()
    btn[0].callback("🔙 Menu", "menu")
    list_active_torrents(0, chat, message, shared)


@bot.callback("add_magnet")
def addmagnet_callback(shared, query, data) -> None:
    shared['status'] = f"magnet#{data}"
    query.notify("Send a magnet link")


@bot.callback("add_torrent")
def addtorrent_callback(shared, query, data) -> None:
    shared['status'] = f"torrent#{data}"
    query.notify("Send a torrent file")


@bot.callback("pause_all")
def pauseall_callback(query) -> None:
    qbittorrent_control.pause_all()
    query.notify("Paused All")


@bot.callback("resume_all")
def resumeall_callback(query) -> None:
    qbittorrent_control.resume_all()
    query.notify("Resumed All")


@bot.callback("pause")
def pause_callback(shared, chat, message, data) -> None:
    if data is None:
        list_active_torrents(1, chat, message, "pause")

    else:
        qbittorrent_control.pause(id_torrent=int(data))
        send_menu(message, chat, shared)


@bot.callback("resume")
def resume_callback(shared, chat, message, data) -> None:
    if data is None:
        list_active_torrents(1, chat, message, "resume")

    else:
        qbittorrent_control.resume(id_torrent=int(data))
        send_menu(message, chat, shared)


@bot.callback("delete_one")
def delete_callback(message, data) -> None:
    btn = botogram.Buttons()
    btn[0].callback("🗑 Delete torrent", "delete_one_no_data", data)
    btn[1].callback("🗑 Delete torrent and data", "delete_one_data", data)
    btn[2].callback("🔙 Menu", "menu")
    message.edit("Qbitorrent Control", attach=btn)


@bot.callback("delete_one_no_data")
def delete_no_data_callback(shared, chat, message, data) -> None:
    if data is None:
        list_active_torrents(1, chat, message, "delete_one_no_data")

    else:
        qbittorrent_control.delete_one_no_data(id_torrent=int(data))
        send_menu(message, chat, shared)


@bot.callback("delete_one_data")
def delete_with_data_callback(shared, chat, message, data) -> None:
    if data is None:
        list_active_torrents(1, chat, message, "delete_one_data")

    else:
        qbittorrent_control.delete_one_data(id_torrent=int(data))
        send_menu(message, chat, shared)


@bot.callback("delete_all")
def delete_all_callback(message) -> None:
    btn = botogram.Buttons()
    btn[0].callback("🗑 Delete all torrents", "delete_all_no_data")
    btn[1].callback("🗑 Delete all torrents and data", "delete_all_data")
    btn[2].callback("🔙 Menu", "menu")
    message.edit("Qbitorrent Control", attach=btn)


@bot.callback("delete_all_no_data")
def delete__all_with_no_data_callback(message, chat, query, shared) -> None:
    qbittorrent_control.delall_no_data()
    query.notify("Deleted only torrents")
    send_menu(message, chat, shared)


@bot.callback("delete_all_data")
def delete_all_with_data_callback(message, chat, query, shared) -> None:
    qbittorrent_control.delall_data()
    query.notify("Deleted All+Torrents")
    send_menu(message, chat, shared)


@bot.callback("torrentInfo")
def torrent_info_callback(message, data) -> None:
    torrent = qbittorrent_control.get_torrent_info(data=int(data))
    progress = torrent.progress * 100
    text = ""

    if progress == 0:
        text += f"{torrent.name}\n[            ] " \
                f"{round(progress, 2)}% completed\n" \
                f"State: {torrent.state.capitalize()}\n" \
                f"Download Speed: {convert_size(torrent.dlspeed)}/s\n" \
                f"Size: {convert_size(torrent.size)}\nETA: " \
                f"{convert_eta(int(torrent.eta))}\n\n"

    elif progress == 100:
        text += f"{torrent.name}\n[completed] " \
                f"{round(progress, 2)}% completed\n" \
                f"State: {torrent.state.capitalize()}\n" \
                f"Upload Speed: {convert_size(torrent.upspeed)}/s\n\n"

    else:
        text += f"{torrent.name}\n[{'=' * int(progress / 10)}" \
                f"{' ' * int(12 - (progress / 10))}]" \
                f" {round(progress, 2)}% completed\n" \
                f"State: {torrent.state.capitalize()} \n" \
                f"Download Speed: {convert_size(torrent.dlspeed)}/s\n" \
                f"Size: {convert_size(torrent.size)}\nETA: " \
                f"{convert_eta(int(torrent.eta))}\n\n"

    btn = botogram.Buttons()
    btn[0].callback("⏸ Pause", "pause", data)
    btn[0].callback("▶️ Resume", "resume", data)
    btn[1].callback("🗑 Delete", "delete_one", data)
    btn[2].callback("🔙 Menu", "menu")

    message.edit(text, attach=btn)


@bot.process_message
def process_message(shared, chat, message) -> None:
    if "magnet" in shared['status']:
        if message.text.startswith("magnet:?xt"):
            magnet_link = message.text.split(" , ")
            category = shared['status'].split("#")[1]
            qbittorrent_control.add_magnet(magnet_link=magnet_link,
                                           category=category)
            send_menu(message, chat, shared)
            shared['status'] = "None"

        else:
            chat.send("This magnet link is invalid! Retry")

    elif "torrent" in shared['status'] and message.document:
        if ".torrent" in message.document.file_name:
            with tempfile.TemporaryDirectory() as tempdir:
                name = f"{tempdir}/{message.document.file_name}"
                category = shared['status'].split("#")[1]
                message.document.save(name)
                qbittorrent_control.add_torrent(file_name=name,
                                                category=category)
            send_menu(message, chat, shared)
            shared['status'] = "None"

        else:
            chat.send("This is not a torrent file! Retry")

    elif shared['status'] == "category_name":
        shared['status'] = f"category_dir#{message.text}"
        chat.send(f"now send me the path for the category {message.text}")

    elif "category_dir" in shared['status']:
        if os.path.exists(message.text):
            name = shared['status'].split("#")[1]

            if "modify" in shared['status']:
                qbittorrent_control.edit_category(name=name,
                                                  save_path=message.text)
                send_menu(message, chat, shared)
                return

            qbittorrent_control.create_category(name=name,
                                                save_path=message.text)
            send_menu(message, chat, shared)

        else:
            chat.send("The path entered does not exist! Retry")


if __name__ == "__main__":
    bot.run()
