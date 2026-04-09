# Migrating to V3

Version 3 of QBittorrentBot introduces significant internal changes, including a full rewrite of the codebase, the switch to **Aiogram**, and new runtime data management via **Redis**. The configuration file format has also changed. This section explains the main differences and what you need to do to migrate from previous versions.

---

## Major Changes in V3

### Project and Libraries

* The entire project has been **rewritten** for better performance and maintainability.
* **UV** ([Universal Virtual Environment](https://docs.astral.sh/uv/)) is now used to manage dependencies and the project environment.
* The Telegram library is now **Aiogram**, a fully asynchronous framework replacing Pyrogram (deprecated).
* **Database support has been removed.** Redis is now used to store all runtime data, statuses, and cached information.
* The bot is now fully asynchronous, more robust, and optimized for larger workloads.

**Future improvements:**

* Implement Aiogram FSM for better state management
* Make the client manager fully asynchronous
* Add internalization (i18n) support using Aiogram

---

### Configuration Changes

The configuration file has been **completely redesigned**:

* Old `config.json` → replaced by **`config.yml`**
* **New fields:**

  * `redis` → Redis connection string for runtime storage
  * `users.notification_filter` → optional filter to limit notifications to certain torrent categories
* Removed Pyrogram-specific fields (`api_id` and `api_hash`). Now **only the Telegram bot token** is required.
* Automatic configuration reload is supported — **most changes take effect without restarting the bot**, except when changing the Telegram bot token or redis url.

For more information please, check the [configuration file](./configuration_file.md) page

---

### V2 vs V3 Configuration

||| V2
```json
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
    "proxy": {
      "scheme": "http",
      "hostname": "myproxy.local",
      "port": 8080,
      "username": "admin",
      "password": "admin"
    }
  },
  "users": [
    {
      "user_id": 123456,
      "notify": false,
      "locale": "en",
      "role": "administrator"
    }
  ]
}
```
||| V3
```yaml
client:
  type: qbittorrent
  host: http://192.168.178.102:8080
  user: admin
  password: admin

redis:
  url: redis://cache:6379/0

telegram:
  bot_token: 1111111:AAAAAAAA-BBBBBBBBB
  proxy:
    scheme: socks5
    hostname: 127.0.0.1
    username: proxyuser
    password: proxypass

users:
  - user_id: 123456
    role: administrator
    notify: true
    notification_filter: movies
    locale: en
```
|||
---
