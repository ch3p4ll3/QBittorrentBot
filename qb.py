#!/usr/local/bin/python3.7
import datetime
import json
from math import log, floor, pow

import botogram
import psutil
import qbittorrentapi
import tempfile

with open("login.json") as login_file:
    data = json.load(login_file)
    bot = botogram.create(data['token'])

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


def convertETA(n) -> str:
    return str(datetime.timedelta(seconds=n))


def login() -> qbittorrentapi.Client:
    ip, port, user, password = data['qbittorrent']['ip'], \
                               data['qbittorrent']['port'],\
                               data['qbittorrent']['user'], \
                               data['qbittorrent']['password']

    qbt_client = qbittorrentapi.Client(host='http://{}:{}'.format(ip, port),
                                       username=user, password=password)
    try:
        qbt_client.auth_log_in()
    except qbittorrentapi.LoginFailed as e:
        print(e)

    return qbt_client


def add_magnet(link, category=None) -> None:
    qbt_client = login()

    cat = category
    if cat == "None":
        cat = None

    if category is not None:
        qbt_client.torrents_add(urls=link, category=cat)
    else:
        qbt_client.torrents_add(urls=link)
    qbt_client.auth_log_out()


def add_torrent(file_name, category=None) -> None:
    qbt_client = login()

    cat = category
    if cat == "None":
        cat = None

    try:
        if category is not None:
            qbt_client.torrents_add(torrent_files=file_name, category=cat)
        else:
            qbt_client.torrents_add(torrent_files=file_name)

    except qbittorrentapi.exceptions.UnsupportedMediaType415Error:
        pass

    qbt_client.auth_log_out()


def resume_all() -> None:
    qbt_client = login()
    qbt_client.torrents.resume.all()
    qbt_client.auth_log_out()


def pause_all() -> None:
    qbt_client = login()
    qbt_client.torrents.pause.all()
    qbt_client.auth_log_out()


def resume(id_torrent) -> None:
    qbt_client = login()
    qbt_client.torrents_resume(hashes=qbt_client.torrents_info()[id_torrent
                                                                 - 1].hash)
    qbt_client.auth_log_out()


def pause(id_torrent) -> None:
    qbt_client = login()
    qbt_client.torrents_pause(hashes=qbt_client.torrents_info()[id_torrent
                                                                - 1].hash)
    qbt_client.auth_log_out()


def delete_one_no_data(id_torrent) -> None:
    qbt_client = login()
    qbt_client.torrents_delete(delete_files=False,
                               hashes=qbt_client.torrents_info()[id_torrent
                                                                 - 1].hash)
    qbt_client.auth_log_out()


def delete_one_data(id_torrent) -> None:
    qbt_client = login()
    qbt_client.torrents_delete(delete_files=True,
                               hashes=qbt_client.torrents_info()[id_torrent
                                                                 - 1].hash)
    qbt_client.auth_log_out()


def delall_no_data() -> None:
    qbt_client = login()
    for i in qbt_client.torrents_info():
        qbt_client.torrents_delete(delete_files=False, hashes=i.hash)
    qbt_client.auth_log_out()


def delall_data() -> None:
    qbt_client = login()
    for i in qbt_client.torrents_info():
        qbt_client.torrents_delete(delete_files=True, hashes=i.hash)
    qbt_client.auth_log_out()


"""def listt(n) -> str:
    text = ""
    a = 1
    qbt_client = login()
    torrents = qbt_client.torrents_info()
    if not torrents:
        qbt_client.auth_log_out()
        return "empty"
    if n == 1:
        for i in torrents:
            progress = i.progress * 100

            if progress == 0:
                text += f"{a}) {i.name}\n[            ] " \
                        f"{round(progress, 2)}% completed\n" \
                        f"State: {i.state.capitalize()}\n" \
                        f"Download Speed: {convert_size(i.dlspeed)}/s\n" \
                        f"Size: {convert_size(i.size)}\nETA: " \
                        f"{convertETA(int(i.eta))}\n\n"

            elif progress == 100:
                text += f"{a}) {i.name}\n[completed] " \
                        f"{round(progress, 2)}% completed\n" \
                        f"State: {i.state.capitalize()}\n" \
                        f"Upload Speed: {convert_size(i.upspeed)}/s\n\n"

            else:
                text += f"{a}) {i.name}\n[{'=' * int(progress / 10)}" \
                        f"{' ' * int(12 - (progress / 10))}]" \
                        f" {round(progress, 2)}% completed\n" \
                        f"State: {i.state.capitalize()} \n" \
                        f"Download Speed: {convert_size(i.dlspeed)}/s\n" \
                        f"Size: {convert_size(i.size)}\nETA: " \
                        f"{convertETA(int(i.eta))}\n\n"
            a += 1

    else:
        for i in torrents:
            progress = i['progress'] * 100

            if progress == 0:
                text += f"{a}) {i.name}\n[            ] " \
                        f"{round(progress, 2)}% completed\n\n"

            elif progress == 100:
                text += f"{a}) {i.name}\n[completed]" \
                        f"{round(progress, 2)}% completed\n\n"

            else:
                text += f"{a}) {i.name}\n[{'=' * int(progress / 10)}" \
                        f"{' ' * int(12 - (progress / 10))}] " \
                        f"{round(progress, 2)}% completed\n\n"

            a += 1
    qbt_client.auth_log_out()
    return text"""


def list_active_torrents(n, chat, message, shared) -> None:
    qbt_client = login()
    torrents = qbt_client.torrents_info()
    if not torrents:
        qbt_client.auth_log_out()
        btn = botogram.Buttons()
        btn[0].callback("🔙 Menu", "menu")
        try:
            message.edit("There are no torrents", attach=btn)
        except Exception:
            chat.send("There are no torrents", attach=btn)
        return

    btn = botogram.Buttons()
    a = 0

    if n == 1:
        for i in torrents:
            btn[a].callback(i.name, shared['status'], str(a))
            a += 1

        btn[a + 1].callback("🔙 Menu", "menu")

        try:
            message.edit_attach(btn)
        except Exception:
            chat.send("Qbitorrent Control", attach=btn)

    else:
        for i in torrents:
            btn[a].callback(i.name, "torrentInfo", str(a))

            a += 1

        btn[a + 1].callback("🔙 Menu", "menu")

        try:
            message.edit_attach(btn)
        except Exception:
            chat.send("Qbitorrent Control", attach=btn)
    qbt_client.auth_log_out()


def send_menu(message, chat) -> None:
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
    try:
        message.edit("Qbitorrent Control", attach=btn)

    except Exception:
        chat.send("Qbitorrent Control", attach=btn)


@bot.command("start")
def start_command(chat) -> None:
    """Start the bot"""
    id = data['id']
    if chat.id in id:
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

        chat.send("Qbitorrent Control", attach=btn)

    else:
        btn = botogram.Buttons()
        btn[0].url("GitHub", "https://github.com/ch3p4ll3/QBittorrentBot/")
        chat.send("You are not authorized to use this bot.", attach=btn)


@bot.command("stats")
def stats_command(chat) -> None:
    id = data['id']
    if chat.id in id:
        qbt_client = login()

        txt = f"""*============SYSTEM============*
*CPU Usage: *{psutil.cpu_percent(interval=None)}%
*CPU Temp: *{psutil.sensors_temperatures()['cpu-thermal'][0][1]}°C
*Free Memory: *{convert_size(psutil.virtual_memory().available)} \
 of {convert_size(psutil.virtual_memory().total)} \
 ({psutil.virtual_memory().percent}%)
*Disks usage: *{convert_size(psutil.disk_usage('/mnt/usb').used)} \
of {convert_size(psutil.disk_usage('/mnt/usb').total)} \
({psutil.disk_usage('/mnt/usb').percent}%)
\n*=========QBITTORRENT=========*
*Qbittorrent Version: * {qbt_client.app_version()}
*Qbittorrent Web API Version:* {qbt_client.app_web_api_version()}
*Default save path: * {qbt_client.app_default_save_path()}
*Active Torrents: *{len(qbt_client.torrents.info.active())}
*Inactive Torrents: *{len(qbt_client.torrents.info.inactive())}"""

        qbt_client.auth_log_out()

        chat.send(txt, syntax="markdown")

    else:
        btn = botogram.Buttons()
        btn[0].url("GitHub", "https://github.com/ch3p4ll3/QBittorrentBot/")
        chat.send("You are not authorized to use this bot.", attach=btn)


@bot.callback("category")
def category(chat, message, data, query, shared) -> None:
    qbt_client = login()

    j = 0
    btn = botogram.Buttons()

    for i in qbt_client.torrent_categories.categories:
        btn[j].callback(i, data, i)
        j += 1
    qbt_client.auth_log_out()

    if j == 0:
        if "magnet" in data:
            addmagnet_callback(shared, query, "#None")

        else:
            addtorrent_callback(shared, query, "#None")

        return

    try:
        message.edit("Choice a category:", attach=btn)
    except Exception:
        chat.send("Choice a category:", attach=btn)


@bot.callback("menu")
def menu(chat, message) -> None:
    send_menu(message, chat)


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
    pause_all()
    query.notify("Paused All")


@bot.callback("resume_all")
def resumeall_callback(query) -> None:
    resume_all()
    query.notify("Resumed All")


@bot.callback("pause")
def pause_callback(shared, chat, message, data) -> None:
    if data is None:
        list_active_torrents(1, chat, message, shared)
        shared['status'] = "pause"

    else:
        id = int(data)
        pause(id)
        send_menu(message, chat)


@bot.callback("resume")
def resume_callback(shared, chat, message, data) -> None:
    if data is None:
        list_active_torrents(1, chat, message, shared)
        shared['status'] = "resume"

    else:
        id = int(data)
        resume(id)
        send_menu(message, chat)


@bot.callback("delete_one")
def delete_callback(message, data) -> None:
    btn = botogram.Buttons()
    btn[0].callback("🗑 Delete torrent", "delete_one_no_data", data)
    btn[1].callback("🗑 Delete torrent and data", "delete_one_data", data)
    message.edit("Qbitorrent Control", attach=btn)


@bot.callback("delete_one_no_data")
def delete_no_data_callback(shared, chat, message, data) -> None:
    shared['status'] = "delete_one_no_data"
    if data is None:
        list_active_torrents(1, chat, message, shared)

    else:
        id = int(data)
        delete_one_no_data(id)
        send_menu(message, chat)


@bot.callback("delete_one_data")
def delete_with_data_callback(shared, chat, message, data) -> None:
    shared['status'] = "delete_one_data"
    if data is None:
        list_active_torrents(1, chat, message, shared)

    else:
        id = int(data)
        delete_one_data(id)
        send_menu(message, chat)


# delete all callback
@bot.callback("delete_all")
def delete_all_callback(message) -> None:
    btn = botogram.Buttons()
    btn[0].callback("🗑 Delete all torrents", "delete_all_no_data")
    btn[1].callback("🗑 Delete all torrents and data", "delete_all_data")
    btn[2].callback("🔙 Menu", "menu")
    message.edit("Qbitorrent Control", attach=btn)


@bot.callback("delete_all_no_data")
def delete__all_with_no_data_callback(message, chat, query) -> None:
    delall_no_data()
    query.notify("Deleted only torrents")
    send_menu(message, chat)


@bot.callback("delete_all_data")
def delete_all_with_data_callback(message, chat, query) -> None:
    delall_data()
    query.notify("Deleted All+Torrents")
    send_menu(message, chat)


@bot.callback("torrentInfo")
def torrent_info_callback(message, data) -> None:
    id = int(data)
    qbt_client = login()

    torrent = qbt_client.torrents_info()[id - 1]
    progress = torrent.progress * 100
    text = ""

    if progress == 0:
        text += f"{torrent.name}\n[            ] " \
                f"{round(progress, 2)}% completed\n" \
                f"State: {torrent.state.capitalize()}\n" \
                f"Download Speed: {convert_size(torrent.dlspeed)}/s\n" \
                f"Size: {convert_size(torrent.size)}\nETA: " \
                f"{convertETA(int(torrent.eta))}\n\n"

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
                f"{convertETA(int(torrent.eta))}\n\n"

    qbt_client.auth_log_out()

    btn = botogram.Buttons()
    btn[0].callback("⏸ Pause", "pause", str(id))
    btn[0].callback("▶️ Resume", "resume", str(id))
    btn[1].callback("🗑 Delete", "delete_one", str(id))
    btn[2].callback("🔙 Menu", "menu")

    message.edit(text, attach=btn)


@bot.process_message
def process_message(shared, chat, message) -> None:
    if "magnet" in shared['status']:
        if message.text.startswith("magnet:?xt"):
            magnet_link = message.text.split(" , ")
            add_magnet(magnet_link, shared['status'].split("#")[1])
            send_menu(message, chat)
            shared['status'] = "None"

        else:
            chat.send("This magnet link is invalid! Retry")

    elif "torrent" in shared['status'] and message.document:
        if ".torrent" in message.document.file_name:
            with tempfile.TemporaryDirectory() as tempdir:
                name = f"{tempdir}/{message.document.file_name}"
                message.document.save(name)
                add_torrent(name, shared['status'].split("#")[1])
            send_menu(message, chat)
            shared['status'] = "None"

        else:
            chat.send("This is not a torrent file! Retry")


if __name__ == "__main__":
    bot.run()
