[![Codacy Badge](https://api.codacy.com/project/badge/Grade/259099080ca24e029a910e3249d32041)](https://app.codacy.com/gh/ch3p4ll3/QBittorrentBot?utm_source=github.com&utm_medium=referral&utm_content=ch3p4ll3/QBittorrentBot&utm_campaign=Badge_Grade)

# QBittorrentBot

With this bot telegram you can manage your qbittorrent with a few simple clicks. Thanks to QBittorrentBot you can have a list of all the files in download / upload, add torrents and magnets.  
You can add more magnets by simply placing one link per line, e.g. 
```
magnet:?xt=...  
magnet:?xt=...  
```
You can also pause, resume, delete and add/remove and modify categories.

## Installation
install dependencies with `pip install -r requirements.txt`, start the bot with `python3 main.py`

## Configuration
With the change of library to [pyrogram](https://docs.pyrogram.org/) you will need the API_ID and API_HASH. Check [here](https://docs.pyrogram.org/intro/quickstart) to find out how to recover them.  
Modify the config.py file by inserting all the data for qbittorrent, the token of the bot, the API ID and HASH and the ids authorized to use the bot (you can know your id through [this](https://t.me/myidbot) bot)

## How to enable the qBittorrent Web UI
On the menu bar, go to **Tools > Options** qBittorrent WEB UI

*   In the new window, choose **Web UI** option
*   Check the **Enable the Web User Interface (Remote control)** option
*   Choose a port (by default 8080)
*   Set username and password (by default username: admin / password: adminadmin)

Click on Ok to save settings.
