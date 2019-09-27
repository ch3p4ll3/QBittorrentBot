#!/usr/local/bin/python3.7
import botogram, os, datetime, json, math
from pony.orm import *
from qbittorrent import Client

with open("login.json") as login_file:
    data = json.load(login_file)
    bot = botogram.create(data['token'])

bot.about = "with this bot you can control qbittorrent from telegram"
bot.owner = "@yourusername"

db = Database()
with open("login.json") as login_file:
    data = json.load(login_file)['database']
    db.bind(provider='mysql', host=data['ip'],
    user=data['user'], passwd=data['password'], db=data['db_name'])

class Qb(db.Entity):
    id = PrimaryKey(int)
    qb = Required(str)

db.generate_mapping(create_tables=True)

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
         data=json.load(login_file)['qbittorrent']
         return (data['ip'], data['port'],
         data['user'], data['password']);

def read_database():
    with db_session:
        p = Qb[0]
        return p.qb

def write_database(status):
    try:
        with db_session:
            Qb[0].qb=status
    except pony.orm.core.ObjectNotFound:
        with db_session:
            qb=Qb(qb=status, id=0)

def convertETA(n):
    return str(datetime.timedelta(seconds = n))

def add_magnet(link):
    ip, port, user, password=open_login_file()
    qb = Client("http://{}:{}".format(ip, port))
    qb.login(user, password)
    qb.download_from_link(link)
    qb.logout()

def add_torrent(file_name):
    ip, port, user, password=open_login_file()
    qb = Client("http://{}:{}".format(ip, port))
    qb.login(user, password)
    torrent_file = open(file_name, 'rb')
    qb.download_from_file(torrent_file)
    os.remove(file_name)
    qb.logout()

def resume_all():
    ip, port, user, password=open_login_file()
    qb = Client("http://{}:{}".format(ip, port))
    qb.login(user, password)
    qb.resume_all()
    qb.logout()

def pause_all():
    ip, port, user, password=open_login_file()
    qb = Client("http://{}:{}".format(ip, port))
    qb.login(user, password)
    qb.pause_all()
    qb.logout()

def resume(id_torrent):
    ip, port, user, password=open_login_file()
    qb = Client("http://{}:{}".format(ip, port))
    qb.login(user, password)
    qb.resume(qb.torrents()[id_torrent-1]['hash'])
    qb.logout()

def pause(id_torrent):
    ip, port, user, password=open_login_file()
    qb = Client("http://{}:{}".format(ip, port))
    qb.login(user, password)
    qb.pause(qb.torrents()[id_torrent-1]['hash'])
    qb.logout()

def delete_one_no_data(id_torrent):
    ip, port, user, password, id=open_login_file()
    qb=Client("http://{}:{}".format(ip, port))
    qb.login(user, password)
    qb.delete(qb.torrents()[id_torrent-1]['hash'])
    qb.logout()

def delete_one_data(id_torrent):
    ip, port, user, password, id=open_login_file()
    qb=Client("http://{}:{}".format(ip, port))
    qb.login(user, password)
    qb.delete_permanently(qb.torrents()[id_torrent-1]['hash'])
    qb.logout()

def delall_no_data():
    try:
        ip, port, user, password, id=open_login_file()
        qb = Client("http://{}:{}".format(ip, port))
        qb.login(user, password)
        for i in qb.torrents():
            qb.delete(i['hash']) #scan all torrents and delete them (only torrent, no data)
        qb.logout()
    except:
        qb.logout()

def delall_data():
    try:
        ip, port, user, password, id=open_login_file()
        qb = Client("http://{}:{}".format(ip, port))
        qb.login(user, password)
        for i in qb.torrents():
            qb.delete_permanently(i['hash']) #scan all torrents and delete them (only torrent, no data)
        qb.logout()
    except:
        qb.logout()


def listt(n):
    l=""
    a=1
    ip, port, user, password=open_login_file()
    qb = Client("http://{}:{}".format(ip, port))
    qb.login(user, password)
    torrents=qb.torrents()
    if not torrents:
        qb.logout()
        return "empty"
    if n==1:
        for i in torrents:
            progress=i['progress']*100

            if progress == 0:
                l+=("{}) {}\n[            ] {}% completed\nState: {}\n"
                "Download Speed: {}/s\nSize: {}\nETA: {}\n\n").format(str(a),
                 i['name'], str(round(progress,2)),i['state'].capitalize(),
                  convert_size(i['dlspeed']), convert_size(i['size'],
                  convertETA(int(i['eta']))))

            elif (progress == 100):
                l+=("{}) {}\n[completed] {}% completed\nState: {}\n"
                "Upload Speed: {}/s\n\n").format(str(a), i['name'], str(round(progress,2)),
                i['state'].capitalize(), convert_size(i['upspeed']))

            else:
                l+=("{}) {}\n[{}{}] {}% completed\nState: {} \n"
                "Download Speed: {}/s\nSize: {}\nETA: {}\n\n").format(str(a),
                i['name'], "="*int(progress/10)," "*int(12-(progress/10)),
                str(round(progress,2)), i['state'].capitalize(),
                convert_size(i['dlspeed']), convert_size(i['size']),
                convertETA(int(i['eta'])))
            a+=1

    else:
        for i in torrents:
            progress=i['progress']*100

            if progress == 0:
                l+="{}) {}\n[            ] {}% completed\n\n".format(str(a),
                i['name'], str(round(progress,2)))

            elif (progress == 100):
                l+="{}) {}\n[completed]{}% completed\n\n".format(str(a),
                i['name'], str(round(progress,2)))

            else:
                l+="{}) {}\n[{}{}] {}% completed\n\n".format(str(a),
                i['name'], "="*int(progress/10), " "*int(12-(progress/10)), str(round(progress,2)))

            a+=1
    qb.logout()
    return l

@bot.command("start")
def greeter_command(chat, message):
    """Start the bot"""
    with open("login.json") as login_file:
        id = json.load(login_file)['id']
    if chat.id == id:
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
        btns=botogram.Buttons()
        btns[0].url("GitHub", "https://github.com/ch3p4ll3/botogramQBittorrent/")
        chat.send("You are not authorized to use this bot.", attach=btns)

@bot.callback("list")
def list_callback(chat, query, data):
    chat.send(listt(1))

@bot.callback("add_magnet")
def list_callback(chat, query, data):
    write_database("magnet")
    query.notify("Send me the magnet link")

@bot.callback("add_torrent")
def list_callback(chat, query, data):
    write_database("torrent")
    query.notify("Send me the torrent file")

@bot.callback("pause_all")
def list_callback(chat, query, data):
    pause_all()
    query.notify("Paused All")

@bot.callback("resume_all")
def list_callback(chat, query, data):
    resume_all()
    query.notify("Resumed All")

@bot.callback("pause")
def list_callback(chat, query, data):
    chat.send(listt(0))
    write_database("pause")

@bot.callback("resume")
def list_callback(chat, query, data):
    chat.send(listt(0))
    write_database("resume")

#delete one torrent callback
@bot.callback("delete_one")
def delete_callback(chat, message, query, data):
    btns=botogram.Buttons()
    btns[0].callback("🗑 Delete Torrent", "delete_one_no_data")
    btns[1].callback("🗑 Delete Torrent+Data", "delete_one_data")
    message.edit("Qbitorrent Control", attach=btns)

@bot.callback("delete_one_no_data")
def delete_no_data_callback(chat, query, data):
    write_database("delete one no data")
    chat.send(listt(0))

@bot.callback("delete_one_data")
def delete_with_data_callback(chat, query, data):
    write_database("delete one data")
    chat.send(listt(0))

#delete all callback
@bot.callback("delete_all")
def delete_all_callback(message, chat, query, data):
    btns=botogram.Buttons()
    btns[0].callback("🗑 Delete All Torrents", "delete_all_no_data")
    btns[1].callback("🗑 Delete All Torrent+Data", "delete_all_data")
    message.edit("Qbitorrent Control", attach=btns)

@bot.callback("delete_all_no_data")
def delete__all_with_no_data_callback(message, chat, query, data):
    delall_no_data()
    query.notify("Deleted All")
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

    message.edit("Qbitorrent Control", attach=btns)

@bot.callback("delete_all_data")
def delete_all_with_data_callback(message, chat, query, data):
    delall_data()
    query.notify("Deleted All+Torrents")
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

    message.edit("Qbitorrent Control", attach=btns)

@bot.process_message
def process_message(chat, message):
    if read_database() == "magnet" and "magnet:?xt" in message.text:
        magnet_link=message.text.split(" , ")
        add_magnet(magnet_link)
        write_database("None")

    elif read_database() == "torrent" and message.document:
        if ".torrent" in message.document.file_name:
            name="/tmp/"+message.document.file_name
            message.document.save(name)
            add_torrent(name)
        write_database("None")

    elif read_database() == "resume":
        try:
            id=int(message.text)
            resume(id)
        except:
            chat.send("wrong id")
        write_database("None")

    elif read_database() == "pause":
        try:
            id=int(message.text)
            pause(id)
        except:
            chat.send("wrong id")
        write_database("None")

    elif read_database() == "delete one no data":
        try:
            id=int(message.text)
            delete_one_no_data(id)
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
        except:
            chat.send("wrong id")
        write_database("None")

    elif read_database() == "delete one data":
        try:
            id=int(message.text)
            delete_one_data(id)
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
        except:
            chat.send("wrong id")
        write_database("None")

if __name__ == "__main__":
    write_database("None")
    bot.run()
