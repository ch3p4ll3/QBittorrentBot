# Add new client manager

Adding a new client manager to QBittorrentBot involves creating a new class that implements the `ClientManager` interface. This interface defines the methods that the bot uses to interact with the client, such as adding, removing, pausing, and resuming torrents.

To do this you need to follow a couple of steps:

- Clone the repository locally using the command: `git clone https://github.com/ch3p4ll3/QBittorrentBot.git`
- Navigate to the folder `src/client_manager`
- Create a new file for your client manager class. Name the file something like `<client>_manager.py`. For example, if you are writing a manager for utorrent the name will be `utorrent_manager.py`
- Define your client manager class. The class should inherit from the `ClientManager` class and implement all of its methods. For example, the `utorrent_manager.py` file might look like this:
```python
from typing import Union, List
from .client_manager import ClientManager


class UtorrentManager(ClientManager):
    @classmethod
    def add_magnet(cls, magnet_link: Union[str, List[str]], category: str = None) -> None:
        # Implement your code to add a magnet to the utorrent client
        pass

    @classmethod
    def add_torrent(cls, file_name: str, category: str = None) -> None:
        # Implement your code to add a torrent to the utorrent client
        pass
...
```
- Navigate to the `src/configs/` folder and edit the `enums.py` file by adding to the `ClientTypeEnum` class an enum for your client. For example, if we wanted to add a manager for utorrent the class would become like this:
```python
class ClientTypeEnum(str, Enum):
    QBittorrent = 'qbittorrent'
    Utorrent = 'utorrent'
```
- Return to the `src/client_manager` folder and edit the `client_repo.py` file by adding to the dictionary named `repositories` an entry associating the newly created enum with the new manager. Example:
```python
from ..configs.enums import ClientTypeEnum
from .qbittorrent_manager import QbittorrentManager, ClientManager


class ClientRepo:
    repositories = {
        ClientTypeEnum.QBittorrent: QbittorrentManager,
        ClientTypeEnum.Utorrent: UtorrentManager
    }
...
```
- Register your client manager in the config file. The config file is a JSON file that defines the configuration for the QBittorrentBot. You can add your new client manager to the client section of the config file. For example, the config file might look like this:
```json
{
    "client": {
        "type": "utorrent",
        "host": "192.168.178.102",
        "port": 8080,
        "user": "admin",
        "password": "admin"
    },
    "telegram": {
        "bot_token": "1111111:AAAAAAAA-BBBBBBBBB",
        "api_id": 1111,
        "api_hash": "aaaaaaaa"
    },

    "users": [
        {
            "user_id": 123456,
            "notify": false,
            "role": "administrator"
        }
    ]
}
```
- Build the docker image
- Start the docker container

You can now use the bot with the new client, have fun:partying_face: