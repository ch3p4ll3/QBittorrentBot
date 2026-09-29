# The story of QBittorrentBot

> [!NOTE]
> **Maintenance status:** I'm no longer actively maintaining this repository. I've changed my workflow and now use the *arr stack, so I don't really use the bot anymore. Every PR is still welcome, though, and I'll update the libraries every once in a while.

QBittorrentBot started with a simple goal: control **qBittorrent** directly from **Telegram**, without having to open the Web UI. Add magnet links or torrent files, see the list of active downloads, pause, resume or delete them, all from a chat.

This document walks through seven years of history, from the first commit on **September 23, 2019** to today: from the first lines built on `botogram`, to the switch to Pyrogram, the big V2 rewrite, and finally the V3 migration to Aiogram.

## The project in numbers

| | |
|---|---|
| **First commit** | September 23, 2019 |
| **Total commits** | 280 (as of September 29, 2026) |
| **Tagged versions** | 9, from `V2` to `V3.1.5` |
| **License** | GPL-3.0 (originally MIT) |
| **Language** | Python (~99%), plus the Dockerfile |
| **Distribution** | Docker image on Docker Hub (`ch3p4ll3/qbittorrent-bot`) |
| **Documentation** | [ch3p4ll3.github.io/QBittorrentBot](https://ch3p4ll3.github.io/QBittorrentBot/) |
| **Translations** | Transifex |

## Timeline

| When | What |
|---|---|
| **Sep 2019** | First commit: `botogramQBittorrent` is born |
| **Oct–Dec 2019** | Database removed, multiple authorized users, switch to `qbittorrent-api` |
| **Jan 2020** | `stats` command with qBittorrent and hardware statistics |
| **Jun 2020** | Categories, Dockerfile, torrent list, first pull requests |
| **Dec 2020** | Database and notifications when a download finishes |
| **Sep 2021** | Migration to **Pyrogram** |
| **Nov 2021** | First external contribution: filter by status in the list |
| **Oct 2022** | Docker and JSON configuration |
| **Oct 2023** | Async client, search by hash |
| **Dec 21, 2023** | **V2**: the big rewrite |
| **Jan 20, 2024** | **V2.1**: localization, proxy, HTTPS |
| **Jan 18, 2026** | **V3.0.0**: Aiogram, YAML, Redis, `uv` |
| **Jan 22, 2026** | **V3.0.1**: async qBittorrent client |
| **Jan 26, 2026** | **V3.1.1**: i18n with Aiogram |
| **Feb 11, 2026** | **V3.1.2**: fix for long names |
| **Apr 12, 2026** | **V3.1.3**: name escaping, category editing |
| **Sep 25, 2026** | **V3.1.4**: qBittorrent 5.1 compatibility |
| **Sep 28, 2026** | **V3.1.5**: Redis backend and notification fixes |

## The origins: `botogramQBittorrent` (2019)

The first commit, on September 23, 2019, was simply titled "Add files via upload". It contained a single script, `qb.py`, of about 350 lines, along with a `login.json` and a README presenting the project as **botogramQBittorrent**: a Python bot to control qBittorrent from Telegram, add downloads from magnet links or torrent files, delete or pause them, and get the list of files being downloaded.

The technical foundations were:

- **botogram2** as the Telegram library
- **python-qbittorrent** to talk to the qBittorrent Web UI
- **Pony ORM** with **MySQL** for data
- Configuration in **`login.json`**, with the qBittorrent address, port and credentials, plus the authorized Telegram ID
- **MIT** license

In the following days came the first refinements: login from file, file sizes, more readable download and upload speeds, better delete options. On October 8, 2019 I **removed the database**, which was too much configuration overhead for such a small bot. November brought a PEP8 cleanup and December added support for **multiple authorized IDs**.

On December 27, 2019 came the first important library change: support for **qBittorrent v4.1.0+** and the switch to **`qbittorrent-api`**, which would stay at the heart of the project for years.

## The growth years: 2020–2022

**January 2020.** With the **`stats`** command, the bot starts showing statistics about qBittorrent and the host's hardware.

**June 2020.** A month of intense work:

- **Categories** introduced, then extended with add, modify and remove
- Code modernized with f-strings and PEP8
- First **Dockerfile**, torrent list and temp folder
- First **pull requests** on the repository, with work developed in a test branch

**Late June 2020.** Decorators for access checks and a validator for the JSON file arrive, along with various optimizations.

**December 2020.** The database comes back, this time for a specific reason: it powers the **notification when a torrent finishes downloading**.

**2021.** The repository gets on Dependabot's radar, with a series of security updates (`urllib3`, `pydantic`). Between July and September the migration to **Pyrogram** happens, developed in the branch of the same name and merged into `master` on September 8, 2021, along with a **systemd** configuration. In November comes the **first external contribution**: Bogdan adds the filter by status in the torrent list and fixes category selection when uploading files.

**2022.** The bot gets picked up again: libraries updated in September, then the **Dockerfile and JSON configuration file**, `.dockerignore` and a database folder. In late October the **`docker-image.yml`** workflow is born, the GitHub Action that builds the Docker image and still keeps Docker Hub up to date today.

## Towards V2: the groundwork (2023)

June 2023 fixes the CI, and October brings some database corrections and a more substantial quick fix: updated libraries, **torrent lookup by hash**, **async** functions and a new `qbittorrent_manager`.

Then, in December, the big one: in just a few days the project is turned upside down.

## V2: the big rewrite (December 21, 2023)

Between December 12 and 20, 2023 I rewrote the structure of the bot, which until then had remained a "script-style" project. The code was split into folders and modules, with a logger, a separate configuration and a client repository. The visible changes:

- **New progress bar** (with `tqdm`)
- **New menu**, reorganized
- **User permissions** with three roles: `reader`, `manager` and `administrator`
- **Editing user and client settings** directly from the bot, with configuration reload
- **Connection check** with qBittorrent
- **Torrent export**
- **Speed limit toggle**
- **Regex filters** and verification of the result when adding a torrent
- **Support for multiple torrent clients**
- **Documentation** written from scratch and published with **Retype**, including a migration guide from V1
- **New configuration file** (`config.json.template`)
- **All Contributors** to recognize the people who contribute
- License changed from **MIT to GPL-3.0** (December 18, 2023)

V2 also introduced the warning still present in the README today: before starting the bot, make sure your configuration is up to date.

## V2.1: localization and polish (January 2024)

Right after V2 came a first wave of fixes (January 2), then three weeks of work on **localization**:

- **Multilingual support** with translation files: English (`en`), Italian (`it`), `ru_UA` and `uk_UA`
- **Transifex** integration, whose bots pushed translations into the repository
- **Proxy settings**
- **HTTPS** support and the ability to use a domain instead of an IP address
- A dedicated section on how to **contribute**
- Fixes to the "user not authorized" message and to the primary key size in the database

V2.1 was released on January 20, 2024, followed by the **CHANGELOG**. In August 2024 **Spanish** (`es`) was added too.

## Two quiet years

Between V2.1 and V3 the repository stayed almost still: a few fixes, the Spanish translation, and a long series of automatic Dependabot updates. The bot did its job and there wasn't much to touch.

## V3: modernization (January 2026)

In January 2026 I rebuilt the foundations of the project.

### V3.0.0 (January 18)

Five intense days, from January 13 to 18, to change the entire Telegram layer:

- Migration to **Aiogram**, fully **async**
- Removed the now-deprecated **Pyrogram** dependency
- **Redis** instead of the database for runtime state and cache (optional, but recommended)
- **Automatic reload** of the configuration
- Project and dependency management with **uv**
- Simplified authentication: only the **`bot_token`** is needed, no more `api_id` and `api_hash`
- Configuration in **`config.yml`** instead of `config.json`, with automatic migration of old files
- New `notification_filter` to choose which categories trigger finished-download notifications
- Rewritten documentation: examples with and without Redis, a `docker-compose.yml` example in the `docker/` folder, FAQ, migration guide and proxy configuration

It was a release with **breaking changes**, and the README still flags it.

### V3.0.1 (January 22)

- **Async** manager for the qBittorrent client
- **ARM** Docker builds (v7 and v8) removed from CI

### V3.1.1 (January 26)

- Translations with **Aiogram i18n**, compiled directly in the Dockerfile
- Updated Italian translation and added **Brazilian Portuguese** (`pt_BR`)
- Custom middleware: if the user's language isn't found, the bot tries the Telegram language first, then the default

### V3.1.2 (February 11)

- Fix for **overly long** torrent names, now limited to 40 characters
- New development Docker images

### V3.1.3 (April 12)

- **Category editing** from the bot
- **Escaping of the torrent name** to avoid problems with special characters
- Updated libraries

### V3.1.4 (September 25)

After two refactors between May and June and a library update in August, compatibility with recent qBittorrent versions arrived:

- The bot accepts the **qBittorrent ≥ 5.1 JSON response** when adding torrents (contributed by Yaroslav Sokolov)
- **Refactor** of the code structure for readability and maintainability

### V3.1.5 (September 28)

The latest version, with two fixes, both by Yaroslav Sokolov:

- The **Redis backend** finally works as intended
- Finished torrents are no longer **re-announced every 10 days**

## How the bot evolved

Looking at the seven years as a whole, a few constant directions stand out:

- **From script to configurable product.** From a single file with one authorized ID to user roles, per-category notifications, multiple clients and settings editable from the bot.
- **Telegram library changed three times.** `botogram` (2019), **Pyrogram** (2021), **Aiogram** (2026): each time for a sturdier stack that's easier to maintain.
- **Database, no database, database, Redis.** Removed in 2019, back in 2020 for notifications, replaced by Redis in 2026.
- **From `login.json` to `config.yml`.** Through `config.json` and a template, with an ever clearer format and automatic migrations.
- **From running by hand to a Docker image.** From the first Dockerfile in 2020 to the GitHub Action in 2022, up to `docker compose up -d` and `uv run python -m src.main`.
- **Increasingly international.** From an English-only bot to English, Italian, Russian, Ukrainian, Spanish and Brazilian Portuguese, with Transifex for anyone who wants to add more.

## Thank you!

An open source project lives thanks to the people who put their hands on it, even for a single line. Thank you to:

- [**Bogdan**](https://github.com/bushig) 💻, for the first external code contribution, in 2021: the filter by status in the torrent list
- [**joey00797**](https://github.com/joey00797) 🌍, for translations
- [**Rodolfo Ortega**](https://github.com/rdfortega) 🌍, for translations
- [**Andrew Miroshnichenko**](https://github.com/fiveh) 💻🐛, for code and bug reports
- [**Yaroslav Sokolov**](https://github.com/SokolovYaroslav) 💻🐛, for qBittorrent 5.1 compatibility, the Redis backend fix and the repeated-notifications fix

Thanks also to the "silent" contributors:

- The **Transifex** community, which makes the bot understandable in multiple languages
- **Dependabot** and **All Contributors**, for constant help keeping dependencies and credits in order
- Everyone who opened an issue, starred the repo, made a fork or used the bot every day

## What now?

As written at the top, I'm no longer actively following the project, but I'm not abandoning it entirely:

- **Pull requests are always welcome**
- I'll update the **libraries** every once in a while
- If you want to help with **translations**, everything is on the [Transifex project](https://app.transifex.com/ch3p4ll3/qbittorrent-bot/)

Thank you all for helping QBittorrentBot grow. 🙏
