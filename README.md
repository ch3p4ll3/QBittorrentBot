![GitHub License](https://img.shields.io/github/license/ch3p4ll3/QBittorrentBot)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/259099080ca24e029a910e3249d32041)](https://app.codacy.com/gh/ch3p4ll3/QBittorrentBot?utm_source=github.com&utm_medium=referral&utm_content=ch3p4ll3/QBittorrentBot&utm_campaign=Badge_Grade)
![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/ch3p4ll3/QBittorrentBot/docker-image.yml)
![Docker Pulls](https://img.shields.io/docker/pulls/ch3p4ll3/qbittorrent-bot)


<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-2-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

# QBittorrentBot

With this bot telegram you can manage your qbittorrent with a few simple clicks. Thanks to QBittorrentBot you can have a list of all the files in download / upload, add torrents and magnets.  
You can add more magnets by simply placing one link per line, e.g. 
```
magnet:?xt=...  
magnet:?xt=...  
```
You can also pause, resume, delete and add/remove and modify categories.

# Table Of Contents
- [QBittorrentBot](#qbittorrentbot)
- [Table Of Contents](#table-of-contents)
  - [Warning!](#warning)
  - [Configuration](#configuration)
    - [Retrieve Telegram API ID and API HASH](#retrieve-telegram-api-id-and-api-hash)
    - [JSON Configuration](#json-configuration)
  - [Running](#running)
    - [Build docker](#build-docker)
    - [Running without docker](#running-without-docker)
  - [Contributing Translations on Transifex](#contributing-translations-on-transifex)
  - [How to enable the qBittorrent Web UI](#how-to-enable-the-qbittorrent-web-ui)
  - [Contributors ✨](#contributors-)


## Warning!
Since version V2, the mapping of the configuration file has been changed. Make sure you have modified it correctly before starting the bot

## Configuration
### Retrieve Telegram API ID and API HASH
With the change of library to [pyrogram](https://docs.pyrogram.org/) you will need the API_ID and API_HASH. Check [here](https://core.telegram.org/api/obtaining_api_id) to find out how to recover them.
### JSON Configuration
Edit the config.json.template file and rename it to config.json. 
The config file is stored in the mounted /app/config/ volume

```json5
{
    "client": {
        "type": "qbittorrent",
        "host": "http://192.168.178.102:8080",
        "user": "admin",
        "password": "admin"
    },
    "telegram": {
        "bot_token": "1111111:AAAAAAAA-BBBBBBBBB",
        "api_id": 1111,
        "api_hash": "aaaaaaaa",
        "proxy": {  // optional
            "scheme": "http",
            "hostname": "myproxy.local",
            "port": 8080,
            "username": "admin",  // optional
            "password": "admin"  // optional
        }
    },

    "users": [
        {
            "user_id": 123456,
            "notify": false,
            "locale": "en",  // optional, default "en"
            "role": "administrator"  // optional, default "administrator"
        },
        {
            "user_id": 78910,
            "notify": true,
            "locale": "it",
            "role": "administrator"
        }
    ]
}
```
Note: If notify is true then the user will receive a notification whenever a torrent has finished downloading

## Running
Pull and run the image with: `docker run -d -v /home/user/docker/QBittorrentBot:/app/config:rw --name qbittorrent-bot ch3p4ll3/qbittorrent-bot:latest`
### Build docker
- Clone this repo ```git clone https://github.com/ch3p4ll3/QBittorrentBot.git```
- Move in the project directory
- Create a config.json file
- Run `docker build -t qbittorrent-bot:latest . && docker run -d -v /home/user/docker/QBittorrentBot:/app/config:rw --name qbittorrent-bot qbittorrent-bot:latest`

### Running without docker
- Clone this repo `git clone https://github.com/ch3p4ll3/QBittorrentBot.git`
- Move in the project directory
- Install dependencies with `pip3 install -r requirements.txt`
- Create a config.json file
- Start the bot with `python3 main.py`

## Contributing Translations on Transifex
QBittorrentBot is an open-source project that relies on the contributions of its community members to provide translations for its users. If you are multilingual and would like to help us make QBittorrentBot more accessible to a wider audience, you can contribute by adding new translations or improving existing ones using Transifex:

- Visit the [QBittorrentBot Transifex Project](https://app.transifex.com/ch3p4ll3/qbittorrentbot/).

- If you don't have a Transifex account, sign up for one. If you already have an account, log in.

- Navigate to the "Languages" tab to view the available languages. Choose the language you want to contribute to.

- Locate the specific string you wish to translate. Please note that the text between "${" and "}" should not be edited, as they are placeholders for dynamic content.

- Click on the string you want to translate, enter your translation in the provided field, and save your changes.

- If your language is not listed, you can request its addition.

- Once you have completed your translations, submit them for review. The project maintainers will review and approve your contributions.

Thank you for helping improve QBittorrentBot with your valuable translations!

## How to enable the qBittorrent Web UI
For the bot to work, it requires qbittorrent to have the web interface active. 
You can activate it by going on the menu bar, go to **Tools > Options** qBittorrent WEB UI

- In the new window, choose **Web UI** option
- Check the **Enable the Web User Interface (Remote control)** option
- Choose a port (by default 8080)
- Set username and password (by default username: admin / password: adminadmin)

Click on Ok to save settings.

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/bushig"><img src="https://avatars.githubusercontent.com/u/2815779?v=4?s=100" width="100px;" alt="Bogdan"/><br /><sub><b>Bogdan</b></sub></a><br /><a href="https://github.com/ch3p4ll3/QBittorrentBot/commits?author=bushig" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/joey00797"><img src="https://avatars.githubusercontent.com/u/52893618?v=4?s=100" width="100px;" alt="joey00797"/><br /><sub><b>joey00797</b></sub></a><br /><a href="#translation-joey00797" title="Translation">🌍</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!
