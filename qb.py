#!/usr/local/bin/python3.7
import botogram
import os
import datetime
import psutil
import json
import math
import qbittorrentapi

with open("login.json") as login_file:
    data = json.load(login_file)
    bot = botogram.create(data['token'])

bot.about = "with this bot you can control qbittorrent from telegram"
bot.owner = "@ch3p4ll3"


@bot.prepare_memory
def prepare_memory(shared):
    shared['status'] = "None"


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


def open_login_file():
    with open("login.json", "r") as login_file:
        data = json.load(login_file)['qbittorrent']
        return (data['ip'], data['port'],
                data['user'], data['password'])


def convertETA(n):
    return str(datetime.timedelta(seconds=n))


def add_magnet(link):
    ip, port, user, password = open_login_file()
    qbt_client = qbittorrentapi.Client(host='http://{}:{}'.format(ip, port),
                                       username=user, password=password)
    try:
        qbt_client.auth_log_in()
    except qbittorrentapi.LoginFailed as e:
        print(e)

    qbt_client.torrents_add(urls=link)
    qbt_client.auth_log_out()


def add_torrent(file_name):
    ip, port, user, password = open_login_file()
    qbt_client = qbittorrentapi.Client(host='http://{}:{}'.format(ip, port),
                                       username=user, password=password)
    try:
        qbt_client.auth_log_in()
    except qbittorrentapi.LoginFailed as e:
        print(e)

    qbt_client.torrents_add(torrent_files=file_name)
    qbt_client.auth_log_out()
    os.remove(file_name)


def resume_all():
    ip, port, user, password = open_login_file()
    qbt_client = qbittorrentapi.Client(host='http://{}:{}'.format(ip, port),
                                       username=user, password=password)
    try:
        qbt_client.auth_log_in()
    except qbittorrentapi.LoginFailed as e:
        print(e)

    qbt_client.torrents.resume.all()
    qbt_client.auth_log_out()


def pause_all():
    ip, port, user, password = open_login_file()
    qbt_client = qbittorrentapi.Client(host='http://{}:{}'.format(ip, port),
                                       username=user, password=password)
    try:
        qbt_client.auth_log_in()
    except qbittorrentapi.LoginFailed as e:
        print(e)

    qbt_client.torrents.pause.all()
    qbt_client.auth_log_out()


def resume(id_torrent):
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


def pause(id_torrent):
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


def delete_one_no_data(id_torrent):
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


def delete_one_data(id_torrent):
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


def delall_no_data():
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


def delall_data():
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


def listt(n):
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
                text += ("{}) {}\n[            ] {}% completed\nState: {}\nD"
                         "ownload Speed: {}/s\nSize: {}\nETA: {}\n\n").format(
                    str(a), i.name, str(round(progress, 2)),
                    i.state.capitalize(), convert_size(i.dlspeed),
                    convert_size(i.size), convertETA(int(i.eta)))

            elif progress == 100:
                text += ("{}) {}\n[completed] {}% completed\nState: {}\n"
                         "Upload Speed: {}/s\n\n").format(
                    str(a), i.name, str(round(progress, 2)),
                    i.state.capitalize(), convert_size(i.upspeed))

            else:
                text += ("{}) {}\n[{}{}] {}% completed\nState: {} \n"
                         "Download Speed: {}/s\nSize: {}\nETA: {}\n\n").format(
                    str(a), i.name, "=" * int(progress / 10),
                    " " * int(12 - (progress / 10)), str(round(progress, 2)),
                    i.state.capitalize(), convert_size(i.dlspeed),
                    convert_size(i.size), convertETA(int(i.eta)))
            a += 1

    else:
        for i in torrents:
            progress = i['progress'] * 100

            if progress == 0:
                text += "{}) {}\n[            ] {}% completed\n\n".format(
                    str(a), i.name, str(round(progress, 2)))

            elif (progress == 100):
                text += "{}) {}\n[completed]{}% completed\n\n".format(
                    str(a), i.name, str(round(progress, 2)))

            else:
                text += "{}) {}\n[{}{}] {}% completed\n\n".format(
                    str(a), i.name, "=" * int(progress / 10),
                    " " * int(12 - (progress / 10)), str(round(progress, 2)))

            a += 1
    qbt_client.auth_log_out()
    return text


def send_menu(message, chat):
    btns = botogram.Buttons()
    btns[0].callback("📝 List", "list")
    btns[1].callback("➕ Add Magnet", "add_magnet")
    btns[1].callback("➕ Add Torrent", "add_torrent")
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
def start_command(chat, message):
    """Start the bot"""
    with open("login.json") as login_file:
        id = json.load(login_file)['id']
    if chat.id in id:
        btns = botogram.Buttons()
        btns[0].callback("📝 List", "list")
        btns[1].callback("➕ Add Magnet", "add_magnet")
        btns[1].callback("➕ Add Torrent", "add_torrent")
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
                    "https://github.com/ch3p4ll3/botogramQBittorrent/")
        chat.send("You are not authorized to use this bot.", attach=btns)


@bot.command("stats")
def stats_command(chat, message):
    with open("login.json") as login_file:
        id = json.load(login_file)['id']
    if chat.id in id:
        ip, port, user, password = open_login_file()
        qbt_client = qbittorrentapi.Client(host='http://{}:{}'.format(ip,
                                                                      port),
                                           username=user, password=password)

        try:
            qbt_client.auth_log_in()
        except qbittorrentapi.LoginFailed as e:
            print(e)

        txt = "*============SYSTEM============*\n" \
              "*CPU Usage: *{}%\n" \
              "*Free Memory: *{} of {} ({}%)\n" \
              "*Disks usage: *{} of {} ({}%)\n" \
              "*CPU Temp: *{}°C\n" \
              "\n*=========QBITTORRENT=========*\n" \
              "*Qbittorrent Version: * {}\n" \
              "*Qbittorrent Web API Version:* {}\n" \
              "*Default save path: * {}\n" \
              "*Active Torrents: *{}\n" \
              "*Inactive Torrents: *{}"

        txt = txt.format(psutil.cpu_percent(interval=None),
                         convert_size(psutil.virtual_memory().available),
                         convert_size(psutil.virtual_memory().total),
                         psutil.virtual_memory().percent,
                         convert_size(psutil.disk_usage('/mnt/usb').used),
                         convert_size(psutil.disk_usage('/mnt/usb').total),
                         psutil.disk_usage('/mnt/usb').percent,
                         psutil.sensors_temperatures()['coretemp'][0][1],
                         qbt_client.app_version(),
                         qbt_client.app_web_api_version(),
                         qbt_client.app_default_save_path(),
                         len(qbt_client.torrents.info.active()),
                         len(qbt_client.torrents.info.inactive()))

        qbt_client.auth_log_out()

        chat.send(txt, syntax="markdown")


@bot.callback("menu")
def menu(query, chat, message):
    send_menu(message, chat)


@bot.callback("list")
def list_callback(chat, message, query, data):
    btns = botogram.Buttons()
    btns[0].callback("🔙 Menu", "menu")
    try:
        message.edit(listt(1), attach=btns)
    except Exception:
        chat.send(listt(1))


@bot.callback("add_magnet")
def addmagnet_callback(shared, chat, query, data):
    shared['status'] = "magnet"
    query.notify("Send me the magnet link")


@bot.callback("add_torrent")
def addtorrent_callback(shared, chat, query, data):
    shared['status'] = "torrent"
    query.notify("Send me the torrent file")


@bot.callback("pause_all")
def pauseall_callback(chat, query, data):
    pause_all()
    query.notify("Paused All")


@bot.callback("resume_all")
def resumeall_callback(chat, query, data):
    resume_all()
    query.notify("Resumed All")


@bot.callback("pause")
def pause_callback(shared, chat, query, data):
    chat.send(listt(0))
    shared['status'] = "pause"


@bot.callback("resume")
def resume_callback(shared, chat, query, data):
    chat.send(listt(0))
    shared['status'] = "resume"


# delete one torrent callback
@bot.callback("delete_one")
def delete_callback(chat, message, query, data):
    btns = botogram.Buttons()
    btns[0].callback("🗑 Delete Torrent", "delete_one_no_data")
    btns[1].callback("🗑 Delete Torrent+Data", "delete_one_data")
    message.edit("Qbitorrent Control", attach=btns)


@bot.callback("delete_one_no_data")
def delete_no_data_callback(shared, chat, query, data):
    shared['status'] = "delete one no data"
    chat.send(listt(0))


@bot.callback("delete_one_data")
def delete_with_data_callback(shared, chat, query, data):
    shared['status'] = "delete one data"
    chat.send(listt(0))


# delete all callback
@bot.callback("delete_all")
def delete_all_callback(message, chat, query, data):
    btns = botogram.Buttons()
    btns[0].callback("🗑 Delete All Torrents", "delete_all_no_data")
    btns[1].callback("🗑 Delete All Torrent+Data", "delete_all_data")
    message.edit("Qbitorrent Control", attach=btns)


@bot.callback("delete_all_no_data")
def delete__all_with_no_data_callback(message, chat, query, data):
    delall_no_data()
    query.notify("Deleted All")
    send_menu(message, chat)


@bot.callback("delete_all_data")
def delete_all_with_data_callback(message, chat, query, data):
    delall_data()
    query.notify("Deleted All+Torrents")
    send_menu(message, chat)


@bot.process_message
def process_message(shared, chat, message):
    if shared['status'] == "magnet" and "magnet:?xt" in message.text:
        magnet_link = message.text.split(" , ")
        add_magnet(magnet_link)
        send_menu(message, chat)
        shared['status'] = "None"

    elif shared['status'] == "torrent" and message.document:
        if ".torrent" in message.document.file_name:
            name = "/tmp/" + message.document.file_name
            message.document.save(name)
            add_torrent(name)
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
