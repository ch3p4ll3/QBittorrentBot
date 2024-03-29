# Configuration File

The configuration file serves as a central repository for all the necessary information that the QBittorrentBot needs to operate effectively. It defines the connection parameters, credentials, and user settings that the bot utilizes to interact with the qBittorrent server and Telegram API.

Below you can find an example of the configuration file:

```json5
{
    "client": {
        "type": "qbittorrent",
        "host": "http://192.168.178.102",
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

Here's a brief overview of the configuration file and its key sections:

- **Clients Section**: Establishes the connection details for the qBittorrent server, including the hostname, port number, username, and password. This enables the bot to interact with the qBittorrent server and manage torrents.

- **Telegram Section**: Contains the bot token, API ID, and API hash, which are essential for authenticating the bot with the Telegram API. These credentials allow the bot to communicate with the Telegram server and receive user commands. Click [here](https://core.telegram.org/api/obtaining_api_id) to find out how to retrive your API ID and API Hash

- **Users Section**: Lists the authorized users of the QBittorrentBot, along with their Telegram user IDs, notification preferences, and user roles. This section defines the users who can interact with the bot, receive notifications, and manage torrents.

## Client

This section defines the configuration for the qBittorrent client that the bot will be interacting with.

Name     | Type                              | Remarks
---      |-----------------------------------| ---
type     | [ClientTypeEnum](#clienttypeenum) | The type of client.
host     | [HttpUrl](#httpurl)               | The IP address of the qBittorrent server.
user     | str                               | The username for the qBittorrent server.
password | str                               | The password for the qBittorrent server.

## Telegram

This section defines the configuration for the Telegram bot that the QBittorrentBot will be communicating with.

Name      | Type                                              | Remarks
---       | ---                                               | ---
bot_token | str                                               | The bot token for the QBittorrentBot. This is a unique identifier that is used to authenticate the bot with the Telegram API.
api_id    | int                                               | The API ID for the QBittorrentBot. This is a unique identifier that is used to identify the bot to the Telegram API.
api_hash  | str                                               | The API hash for the QBittorrentBot. This is a string of characters that is used to verify the authenticity of the bot's requests to the Telegram API.
proxy     | [TelegramProxySettings](#telegram-proxy-settings) | Optional, the settings for using a proxy to contact telegram servers


## Users

This section defines the list of users who are authorized to use the QBittorrentBot. Each user is defined by their Telegram user ID, whether or not they should be notified about completed torrents, and their role.

Name     | Type                            | Remarks
---      | ---                             | ---
user_id  | int                             | The Telegram user ID of the user. This is a unique identifier that is used to identify the user to the Telegram API.
notify   | bool                            | Whether or not the user should be notified about new torrents.
role     | [UserRolesEnum](#userrolesenum) | The role of the user. Default: `administrator`
locale   | str                             | Language used by the user, [list of supported languages](#languages). Default: `en`

## Enums

### ClientTypeEnum

Name        | Type   | Value(to be used in json)
---         | ---    |---
QBittorrent | str    | `qbittorrent`

### UserRolesEnum
Name         | Type   | Value(to be used in json) | Remarks
---          | ---    |---                        | 
Reader       | str    | `reader`                    | Can perform only reading operations(view torrents)
Manager      | str    | `manager`                   | Can perform only managing operations(view torrents + can download files + can add/edit categories + set torrent priority + can stop/start downloads)
Administrator| str    | `administrator`             | Can perform all operations (Manager + remove torrent + remove category + edit configs)

### Telegram Proxy Scheme
Name        | Type   | Value(to be used in json)
---         | ---    |---
Sock4       | str    | `socks4`
Sock5       |str     | `socks5`
Http        |str     | `http`

## Other types

### HttpUrl
A type that will accept any http or https URL.
- TLD required
- Host required
- Max length 2083

### Languages
Name             | Type   | Value(to be used in json)
---              | ---    |---
English          | str    | `en`
Italian          | str    | `it`
Ukrainian        | str    | `uk_UA`
Russian(Ukraine) | str    | `ru_UA`

### Telegram Proxy Settings
QBittorrentBot supports proxies with and without authentication. This feature allows QBittorrentBot to exchange data with Telegram through an intermediate SOCKS 4/5 or HTTP proxy server.

Name       | Type                                          | Remarks
---        | ---                                           | ---
scheme     | [TelegramProxyScheme](#telegram-proxy-scheme) | The scheme to be used to connect to the proxy
hostname   | str                                           | The hostname of the proxy
username   | str                                           | Optional, the proxy user
password   | str                                           | Optional, the proxy password