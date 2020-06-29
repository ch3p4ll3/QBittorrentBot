import qbittorrentapi
from json_validation import get_configs


def qbittorrentLogin(func):
    def wrapper(**kwargs):

        qbt_client = qbittorrentapi.Client(
            host=f'http://{get_configs().qbittorrent.ip}:'
                 f'{get_configs().qbittorrent.port}',
            username=get_configs().qbittorrent.user,
            password=get_configs().qbittorrent.password)

        try:
            qbt_client.auth_log_in()
        except qbittorrentapi.LoginFailed as e:
            print(e)

        resp = func(qbt_client, **kwargs)

        qbt_client.auth_log_out()

        return resp

    return wrapper


@qbittorrentLogin
def add_magnet(qbt_client, magnet_link, category=None) -> None:
    cat = category
    if cat == "None":
        cat = None

    if category is not None:
        qbt_client.torrents_add(urls=magnet_link, category=cat)
    else:
        qbt_client.torrents_add(urls=magnet_link)


@qbittorrentLogin
def add_torrent(qbt_client, file_name, category=None) -> None:
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


@qbittorrentLogin
def resume_all(qbt_client) -> None:
    qbt_client.torrents.resume.all()


@qbittorrentLogin
def pause_all(qbt_client) -> None:
    qbt_client.torrents.pause.all()


@qbittorrentLogin
def resume(qbt_client, id_torrent) -> None:
    qbt_client.torrents_resume(hashes=qbt_client.torrents_info()[id_torrent
                                                                 - 1].hash)


@qbittorrentLogin
def pause(qbt_client, id_torrent) -> None:
    qbt_client.torrents_pause(hashes=qbt_client.torrents_info()[id_torrent
                                                                - 1].hash)


@qbittorrentLogin
def delete_one_no_data(qbt_client, id_torrent) -> None:
    qbt_client.torrents_delete(delete_files=False,
                               hashes=qbt_client.torrents_info()[id_torrent
                                                                 - 1].hash)


@qbittorrentLogin
def delete_one_data(qbt_client, id_torrent) -> None:
    qbt_client.torrents_delete(delete_files=True,
                               hashes=qbt_client.torrents_info()[id_torrent
                                                                 - 1].hash)


@qbittorrentLogin
def delall_no_data(qbt_client) -> None:
    for i in qbt_client.torrents_info():
        qbt_client.torrents_delete(delete_files=False, hashes=i.hash)


@qbittorrentLogin
def delall_data(qbt_client) -> None:
    for i in qbt_client.torrents_info():
        qbt_client.torrents_delete(delete_files=True, hashes=i.hash)


@qbittorrentLogin
def get_categories(qbt_client):
    categories = qbt_client.torrent_categories.categories
    if len(categories) > 0:
        return categories

    else:
        return None


@qbittorrentLogin
def get_torrent_info(qbt_client, data):
    return qbt_client.torrents_info()[int(data) - 1]


@qbittorrentLogin
def edit_category(qbt_client, name, save_path):
    qbt_client.torrents_edit_category(name=name,
                                      save_path=save_path)


@qbittorrentLogin
def create_category(qbt_client, name, save_path):
    qbt_client.torrents_create_category(name=name,
                                        save_path=save_path)


@qbittorrentLogin
def remove_category(qbt_client, data):
    qbt_client.torrents_remove_categories(categories=data)


@qbittorrentLogin
def get_torrent_infos(qbt_client):
    return qbt_client.torrents_info()
