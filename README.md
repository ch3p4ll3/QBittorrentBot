![GitHub License](https://img.shields.io/github/license/ch3p4ll3/QBittorrentBot)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/259099080ca24e029a910e3249d32041)](https://app.codacy.com/gh/ch3p4ll3/QBittorrentBot?utm_source=github.com&utm_medium=referral&utm_content=ch3p4ll3/QBittorrentBot&utm_campaign=Badge_Grade)
![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/ch3p4ll3/QBittorrentBot/docker-image.yml)
![Docker Pulls](https://img.shields.io/docker/pulls/ch3p4ll3/qbittorrent-bot)


<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-3-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

# QBittorrentBot

QBittorrentBot is a Telegram bot that allows you to control your **qBittorrent** client directly through Telegram. With this bot, you can manage your torrent downloads, add magnet links, and much more—all from within your chat.

You can add multiple magnet links by simply placing one per line:

```
magnet:?xt=...
magnet:?xt=...
```

The bot allows you to:

* **List active torrents**
* **Pause/resume torrents**
* **Delete torrents**
* **Add, remove, and modify categories**

# Table of Contents

* [QBittorrentBot](#qbittorrentbot)
* [Table Of Contents](#table-of-contents)

  * [Warning!](#warning)
  * [Configuration](#configuration)

    * [Retrieve Telegram API ID and API HASH](#retrieve-telegram-api-id-and-api-hash)
    * [YAML Configuration](#yaml-configuration)
  * [Running](#running)

    * [Build Docker](#build-docker)
    * [Running Without Docker](#running-without-docker)
  * [Contributing Translations on Transifex](#contributing-translations-on-transifex)
  * [How to Enable the qBittorrent Web UI](#how-to-enable-the-qbittorrent-web-ui)
  * [Contributors ✨](#contributors-)

## Warning!

Since version **V2**, the configuration format has changed. Please ensure your configuration file is updated correctly before starting the bot.

## Configuration

### Retrieve Telegram API ID and API HASH

As part of the transition to **Aiogram**, you no longer need the **API_ID** and **API_HASH**. You only need your **bot_token** to authenticate with the Telegram API.

### YAML Configuration

QBittorrentBot now uses a **YAML** configuration file, replacing the old **JSON** format. The new configuration format includes settings for the qBittorrent client, Telegram bot, Redis (optional), and user roles.

Here’s an example configuration (`config.yml`):

```yaml
client:
  type: qbittorrent
  host: http://localhost:8080/
  user: admin
  password: adminadmin

redis:
  url: redis://localhost:6379/0

telegram:
  bot_token: PUT_YOUR_TELEGRAM_BOT_TOKEN_HERE
  proxy: null

users:
  - user_id: 123456789
    role: administrator
    notify: true
    notification_filter: null
    locale: en

  - user_id: 987654321
    role: manager
    notify: true
    notification_filter:
      - Movies
      - TV
    locale: es

  - user_id: 192837465
    role: reader
    notify: false
    notification_filter: null
    locale: it
```

* **`client`**: Configuration for the **qBittorrent** client (host, username, password).
* **`telegram`**: Telegram bot settings (bot token, proxy settings if applicable).
* **`redis`**: Optional, for Redis configuration (useful for persistence and session management).
* **`users`**: List of users, each with settings for notifications, locale, and role.

### Important:

* If **`notify`** is set to `true`, the user will receive notifications when a torrent finishes downloading.

## Running

### Build Docker

To run **QBittorrentBot** with Docker, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/ch3p4ll3/QBittorrentBot.git
   ```

2. Move into the project directory:

   ```bash
   cd QBittorrentBot
   ```

3. Create your **`config.yml`** file.

4. In the project folder, navigate to the `docker/` directory, where the `docker-compose.yml` example file is located.

   ```bash
   docker compose up -d
   ```

The `docker-compose.yml` file should already be pre-configured for you. It will automatically build the image and start the container.

This method will also mount the `/app/config/` volume, ensuring that the bot uses your configuration settings.

### Running Without Docker

If you prefer to run the bot without Docker, you can follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/ch3p4ll3/QBittorrentBot.git
   ```

2. Move into the project directory:

   ```bash
   cd QBittorrentBot
   ```

3. Install dependencies:

   ```bash
   pip3 install -r requirements.txt
   ```

4. Create your **`config.yml`** file.

5. Start the bot:

   ```bash
   python3 main.py
   ```

## Contributing Translations on Transifex

**QBittorrentBot** is an open-source project that thrives with contributions from the community. If you’re multilingual and want to help make **QBittorrentBot** accessible to more users, you can contribute translations via Transifex.

Here’s how you can help:

1. Visit the [QBittorrentBot Transifex Project](https://app.transifex.com/ch3p4ll3/qbittorrentbot/).
2. Sign up or log in to your Transifex account.
3. Navigate to the "Languages" tab and select the language you’d like to contribute to.
4. Find the string you want to translate and submit your translation.
5. If your language isn’t listed, you can request its addition.
6. Once your translations are reviewed and approved, they will be included in the project.

Thank you for contributing!

## How to Enable the qBittorrent Web UI

To allow the bot to interact with your **qBittorrent** client, you need to enable the **Web UI**. Here’s how to do it:

1. Open **qBittorrent** and go to the menu bar.
2. Navigate to **Tools > Options**.
3. In the new window, select the **Web UI** tab.
4. Enable **Enable the Web User Interface (Remote control)**.
5. Choose a port (default is **8080**).
6. Set a **username** and **password** (default: **admin** / **adminadmin**).

Click **OK** to save the settings.

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
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/rdfortega"><img src="https://avatars.githubusercontent.com/u/19917918?v=4?s=100" width="100px;" alt="Rodolfo Ortega"/><br /><sub><b>Rodolfo Ortega</b></sub></a><br /><a href="#translation-rdfortega" title="Translation">🌍</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=ch3p4ll3/QBittorrentBot&type=Date)](https://star-history.com/#ch3p4ll3/QBittorrentBot&Date)
