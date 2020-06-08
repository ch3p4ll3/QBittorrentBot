#!/usr/local/bin/python3.7
import datetime
import json
import math
import os

import botogram
import psutil
import qbittorrentapi

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
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


def open_login_file() -> tuple:
    with open("login.json", "r") as login_file:
        data = json.load(login_file)['qbittorrent']
        return (data['ip'], data['port'],
                data['user'], data['password'])


def convertETA(n) -> str:
    return str(datetime.timedelta(seconds=n))


def add_magnet(link, category=None) -> None:
    ip, port, user, password = open_login_file()
    qbt_client = qbittorrentapi.Client(host='http://{}:{}'.format(ip, port),
                                       username=user, password=password)
    try:
        qbt_client.auth_log_in()
    except qbittorrentapi.LoginFailed as e:
        print(e)

    cat = category
    if cat == "None":
        cat = None

    if category is not None:
        qbt_client.torrents_add(urls=link, category=cat)
    else:
        qbt_client.torrents_add(urls=link)
    qbt_client.auth_log_out()


def add_torrent(file_name, category=None) -> None:
    ip, port, user, password = open_login_file()
    qbt_client = qbittorrentapi.Client(host='http://{}:{}'.format(ip, port),
                                       username=user, password=password)
    try:
        qbt_client.auth_log_in()
    except qbittorrentapi.LoginFailed as e:
        print(e)

    cat = category
    if cat == "None":
        cat = None

    if category is not None:
        qbt_client.torrents_add(torrent_files=file_name, category=cat)
    else:
        qbt_client.torrents_add(torrent_files=file_name)

    qbt_client.auth_log_out()
    os.remove(file_name)


def resume_all() -> None:
    ip, port, user, password = open_login_file()
    qbt_client = qbittorrentapi.Client(host='http://{}:{}'.format(ip, port),
                                       username=user, password=password)
    try:
        qbt_client.auth_log_in()
    except qbittorrentapi.LoginFailed as e:
        print(e)

    qbt_client.torrents.resume.all()
    qbt_client.auth_log_out()


def pause_all() -> None:
    ip, port, user, password = open_login_file()
    qbt_client = qbittorrentapi.Client(host='http://{}:{}'.format(ip, port),
                                       username=user, password=password)
    try:
        qbt_client.auth_log_in()
    except qbittorrentapi.LoginFailed as e:
        print(e)

    qbt_client.torrents.pause.all()
    qbt_client.auth_log_out()


def resume(id_torrent) -> None:
    ip, port, user, password = open_login_file()
    qbt_client = qbittorrentapi.Client(host='http://{}:{}'.format(ip, port),
                                       username=user, password=password)
    try:
        qbt_client.auth_log_in()
    except qbittorrentapi.LoginFailed as e:
        print(e)

    qbt_client.torrents_resume(hashes=qbt_client.torrents_info()[id_torrent
                                                                 - 1].hash)
    qbt_client.auth_log_out()


def pause(id_torrent) -> None:
    ip, port, user, password = open_login_file()
    qbt_client = qbittorrentapi.Client(host='http://{}:{}'.format(ip, port),
                                       username=user, password=password)
    try:
        qbt_client.auth_log_in()
    except qbittorrentapi.LoginFailed as e:
        print(e)

    qbt_client.torrents_pause(hashes=qbt_client.torrents_info()[id_torrent
                                                                - 1].hash)
    qbt_client.auth_log_out()


def delete_one_no_data(id_torrent) -> None:
    ip, port, user, password = open_login_file()
    qbt_client = qbittorrentapi.Client(host='http://{}:{}'.format(ip, port),
                                       username=user, password=password)
    try:
        qbt_client.auth_log_in()
    except qbittorrentapi.LoginFailed as e:
        print(e)

    qbt_client.torrents_delete(delete_files=False,
                               hashes=qbt_client.torrents_info()[id_torrent
                                                                 - 1].hash)
    qbt_client.auth_log_out()


def delete_one_data(id_torrent) -> None:
    ip, port, user, password = open_login_file()
    qbt_client = qbittorrentapi.Client(host='http://{}:{}'.format(ip, port),
                                       username=user, password=password)
    try:
        qbt_client.auth_log_in()
    except qbittorrentapi.LoginFailed as e:
        print(e)

    qbt_client.torrents_delete(delete_files=True,
                               hashes=qbt_client.torrents_info()[id_torrent
                                                                 - 1].hash)
    qbt_client.auth_log_out()


def delall_no_data() -> None:
    ip, port, user, password = open_login_file()
    qbt_client = qbittorrentapi.Client(host='http://{}:{}'.format(ip, port),
                                       username=user, password=password)
    try:
        qbt_client.auth_log_in()
    except qbittorrentapi.LoginFailed as e:
        print(e)

    for i in qbt_client.torrents_info():
        qbt_client.torrents_delete(delete_files=False, hashes=i.hash)
    qbt_client.auth_log_out()


def delall_data() -> None:
    ip, port, user, password = open_login_file()
    qbt_client = qbittorrentapi.Client(host='http://{}:{}'.format(ip, port),
                                       username=user, password=password)
    try:
        qbt_client.auth_log_in()
    except qbittorrentapi.LoginFailed as e:
        print(e)

    for i in qbt_client.torrents_info():
        qbt_client.torrents_delete(delete_files=True, hashes=i.hash)
    qbt_client.auth_log_out()


def listt(n) -> str:
    text = ""
    a = 1
    ip, port, user, password = open_login_file()
    qbt_client = qbittorrentapi.Client(host='http://{}:{}'.format(ip, port),
                                       username=user, password=password)
    try:
        qbt_client.auth_log_in()
    except qbittorrentapi.LoginFailed as e:
        print(e)
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
    return text


def send_menu(message, chat) -> None:
    btns = botogram.Buttons()
    btns[0].callback("📝 List", "list")
    btns[1].callback("➕ Add Magnet", "category", "add_magnet")
    btns[1].callback("➕ Add Torrent", "category", "add_torrent")
    btns[2].callback("⏸ Pause", "pause")
    btns[2].callback("▶️ Resume", "resume")
    btns[3].callback("⏸ Pause All", "pause_all")
    btns[3].callback("▶️ Resume All", "resume_all")
    btns[4].callback("🗑 Delete", "delete_one")
    btns[4].callback("🗑 Delete All", "delete_all")
    try:
        message.edit("Qbitorrent Control", attach=btns)

    except Exception:
        chat.send("Qbitorrent Control", attach=btns)


@bot.command("start")
def start_command(chat) -> None:
    """Start the bot"""
    id = data['id']
    if chat.id in id:
        btns = botogram.Buttons()
        btns[0].callback("📝 List", "list")
        btns[1].callback("➕ Add Magnet", "category", "add_magnet")
        btns[1].callback("➕ Add Torrent", "category", "add_torrent")
        btns[2].callback("⏸ Pause", "pause")
        btns[2].callback("▶️ Resume", "resume")
        btns[3].callback("⏸ Pause All", "pause_all")
        btns[3].callback("▶️ Resume All", "resume_all")
        btns[4].callback("🗑 Delete", "delete_one")
        btns[4].callback("🗑 Delete All", "delete_all")

        chat.send("Qbitorrent Control", attach=btns)

    else:
        btns = botogram.Buttons()
        btns[0].url("GitHub",
                    "https://github.com/ch3p4ll3/QBittorrentBot/")
        chat.send("You are not authorized to use this bot.", attach=btns)


@bot.command("stats")
def stats_command(chat) -> None:
    id = data['id']
    if chat.id in id:
        ip, port, user, password = open_login_file()
        qbt_client = qbittorrentapi.Client(host='http://{}:{}'.format(ip,
                                                                      port),
                                           username=user, password=password)

        try:
            qbt_client.auth_log_in()
        except qbittorrentapi.LoginFailed as e:
            print(e)

        txt = f"""*============SYSTEM============*
*CPU Usage: *{psutil.cpu_percent(interval=None)}%
*CPU Temp: *{psutil.sensors_temperatures()['coretemp'][0][1]}°C
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
        btns = botogram.Buttons()
        btns[0].url("GitHub",
                    "https://github.com/ch3p4ll3/QBittorrentBot/")
        chat.send("You are not authorized to use this bot.", attach=btns)


@bot.callback("category")
def category(chat, message, data, query, shared):
    ip, port, user, password = open_login_file()
    qbt_client = qbittorrentapi.Client(host='http://{}:{}'.format(ip, port),
                                       username=user, password=password)
    try:
        qbt_client.auth_log_in()
    except qbittorrentapi.LoginFailed as e:
        print(e)

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
def list_callback(chat, message) -> None:
    btns = botogram.Buttons()
    btns[0].callback("🔙 Menu", "menu")
    try:
        message.edit(listt(1), attach=btns)
    except Exception:
        chat.send(listt(1))


@bot.callback("add_magnet")
def addmagnet_callback(shared, query, data) -> None:
    shared['status'] = f"magnet#{data}"
    query.notify("Send me the magnet link")


@bot.callback("add_torrent")
def addtorrent_callback(shared, query, data) -> None:
    shared['status'] = f"torrent#{data}"
    query.notify("Send me the torrent file")


@bot.callback("pause_all")
def pauseall_callback(query) -> None:
    pause_all()
    query.notify("Paused All")


@bot.callback("resume_all")
def resumeall_callback(query) -> None:
    resume_all()
    query.notify("Resumed All")


@bot.callback("pause")
def pause_callback(shared, chat) -> None:
    chat.send(listt(0))
    shared['status'] = "pause"


@bot.callback("resume")
def resume_callback(shared, chat) -> None:
    chat.send(listt(0))
    shared['status'] = "resume"


# delete one torrent callback
@bot.callback("delete_one")
def delete_callback(message) -> None:
    btns = botogram.Buttons()
    btns[0].callback("🗑 Delete Torrent", "delete_one_no_data")
    btns[1].callback("🗑 Delete Torrent+Data", "delete_one_data")
    message.edit("Qbitorrent Control", attach=btns)


@bot.callback("delete_one_no_data")
def delete_no_data_callback(shared, chat) -> None:
    shared['status'] = "delete one no data"
    chat.send(listt(0))


@bot.callback("delete_one_data")
def delete_with_data_callback(shared, chat) -> None:
    shared['status'] = "delete one data"
    chat.send(listt(0))


# delete all callback
@bot.callback("delete_all")
def delete_all_callback(message) -> None:
    btns = botogram.Buttons()
    btns[0].callback("🗑 Delete All Torrents", "delete_all_no_data")
    btns[1].callback("🗑 Delete All Torrent+Data", "delete_all_data")
    message.edit("Qbitorrent Control", attach=btns)


@bot.callback("delete_all_no_data")
def delete__all_with_no_data_callback(message, chat, query) -> None:
    delall_no_data()
    query.notify("Deleted All")
    send_menu(message, chat)


@bot.callback("delete_all_data")
def delete_all_with_data_callback(message, chat, query) -> None:
    delall_data()
    query.notify("Deleted All+Torrents")
    send_menu(message, chat)


@bot.process_message
def process_message(shared, chat, message) -> None:
    if "magnet" in shared['status'] and "magnet:?xt" in message.text:
        magnet_link = message.text.split(" , ")
        add_magnet(magnet_link, shared['status'].split("#")[1])
        send_menu(message, chat)
        shared['status'] = "None"

    elif "torrent" in shared['status'] and message.document:
        if ".torrent" in message.document.file_name:
            name = "/tmp/" + message.document.file_name
            message.document.save(name)
            add_torrent(name, shared['status'].split("#")[1])
            send_menu(message, chat)
        shared['status'] = "None"

    elif shared['status'] == "resume":
        try:
            id = int(message.text)
            resume(id)
            send_menu(message, chat)
        except Exception:
            chat.send("wrong id")
        shared['status'] = "None"

    elif shared['status'] == "pause":
        try:
            id = int(message.text)
            pause(id)
            send_menu(message, chat)
        except Exception:
            chat.send("wrong id")
        shared['status'] = "None"

    elif shared['status'] == "delete one no data":
        try:
            id = int(message.text)
            delete_one_no_data(id)
            send_menu(message, chat)
        except Exception as e:
            print(e)
            chat.send("wrong id")
        shared['status'] = "None"

    elif shared['status'] == "delete one data":
        try:
            id = int(message.text)
            delete_one_data(id)
            send_menu(message, chat)
        except Exception as e:
            print(e)
            chat.send("wrong id")
        shared['status'] = "None"


if __name__ == "__main__":
    bot.run()
