# QBittorrentBot

With this bot telegram you can manage your qbittorrent with a few simple clicks. Thanks to botogramQBittorrent you can have a list of all the files in download / upload, add torrents and magnets (You can add more magnets at a time by simplifying each link with a space, a comma and another space es. `magnet:?xt= , magnet:?xt= , ...`), pause, resume and delete the files.

## Installation
To use the bot you will need the "qbittorrent-api" library and the "botogram2" library and active the QBittorrent web UI interface

`pip install -r requirements.txt`

## Configuration
Edit the login.json file by putting the address, port, username and password of the Qbittorrent web UI. Also change the id authorized to use the bot and the token taken from botfather. Change line 9 by putting your Telegram username.

## How to enable the qBittorrent Web UI
On the menu bar, go to **Tools > Options** qBittorrent WEB UI

*   In the new window, choose **Web UI** option

*   Check the **Enable the Web User Interface (Remote control)** option

*   Choose a port (by default 8080)

*   Set username and password (by default username: admin / password: adminadmin)

Click on Ok to save settings.
