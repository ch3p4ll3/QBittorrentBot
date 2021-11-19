import qbittorrentapi

from config import QBITTORRENT_IP, QBITTORRENT_PSW, QBITTORRENT_USER, QBITTORRENT_PORT


def qbittorrent_login(func):
    def wrapper(*args, **kwargs):

        qbt_client = qbittorrentapi.Client(
            host=f'http://{QBITTORRENT_IP}:'
                 f'{QBITTORRENT_PORT}',
            username=QBITTORRENT_USER,
            password=QBITTORRENT_PSW)

        try:
            qbt_client.auth_log_in()
        except qbittorrentapi.LoginFailed as e:
            print(e)

        resp = func(qbt_client, *args, **kwargs)

        qbt_client.auth_log_out()

        return resp

    return wrapper


@qbittorrent_login
def add_magnet(qbt_client, magnet_link: str, category: str = None) -> None:
    cat = category
    if cat == "None":
        cat = None

    if category is not None:
        qbt_client.torrents_add(urls=magnet_link, category=cat)
    else:
        qbt_client.torrents_add(urls=magnet_link)


@qbittorrent_login
def add_torrent(qbt_client, file_name: str, category: str = None) -> None:
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


@qbittorrent_login
def resume_all(qbt_client) -> None:
    qbt_client.torrents.resume.all()


@qbittorrent_login
def pause_all(qbt_client) -> None:
    qbt_client.torrents.pause.all()


@qbittorrent_login
def resume(qbt_client, id_torrent: int) -> None:
    qbt_client.torrents_resume(hashes=qbt_client.torrents_info()[id_torrent
                                                                 - 1].hash)


@qbittorrent_login
def pause(qbt_client, id_torrent: int) -> None:
    qbt_client.torrents_pause(hashes=qbt_client.torrents_info()[id_torrent
                                                                - 1].hash)


@qbittorrent_login
def delete_one_no_data(qbt_client, id_torrent: int) -> None:
    qbt_client.torrents_delete(delete_files=False,
                               hashes=qbt_client.torrents_info()[id_torrent
                                                                 - 1].hash)


@qbittorrent_login
def delete_one_data(qbt_client, id_torrent: int) -> None:
    qbt_client.torrents_delete(delete_files=True,
                               hashes=qbt_client.torrents_info()[id_torrent
                                                                 - 1].hash)


@qbittorrent_login
def delall_no_data(qbt_client) -> None:
    for i in qbt_client.torrents_info():
        qbt_client.torrents_delete(delete_files=False, hashes=i.hash)


@qbittorrent_login
def delall_data(qbt_client) -> None:
    for i in qbt_client.torrents_info():
        qbt_client.torrents_delete(delete_files=True, hashes=i.hash)


@qbittorrent_login
def get_categories(qbt_client):
    categories = qbt_client.torrent_categories.categories
    if len(categories) > 0:
        return categories

    else:
        return


@qbittorrent_login
def get_torrent_info(qbt_client, data: str = None, status_filter: str = None, ):
    if data is None:
        return qbt_client.torrents_info(status_filter=status_filter)
    return qbt_client.torrents_info(status_filter=status_filter)[int(data) - 1]


@qbittorrent_login
def edit_category(qbt_client, name: str, save_path: str) -> None:
    qbt_client.torrents_edit_category(name=name,
                                      save_path=save_path)


@qbittorrent_login
def create_category(qbt_client, name: str, save_path: str) -> None:
    qbt_client.torrents_create_category(name=name,
                                        save_path=save_path)


@qbittorrent_login
def remove_category(qbt_client, data: str) -> None:
    qbt_client.torrents_remove_categories(categories=data)
