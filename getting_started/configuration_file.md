# Configuration File

The configuration file serves as a central repository for all the necessary information that the QBittorrentBot needs to operate effectively. It defines connection parameters, credentials, and user settings that the bot uses to interact with the qBittorrent server, Telegram API, and optionally Redis.

The bot automatically reloads most configuration changes at runtime. ⚠️ **However, if you update the Telegram bot token or the redis url, you must restart the bot.**

---

## Example Configuration File

```yaml
client:
  host: http://localhost:8080/
  password: adminadmin
  type: qbittorrent
  user: admin
redis:
  url: null
telegram:
  bot_token: PUT_YOUR_TELEGRAM_BOT_TOKEN_HERE
  proxy: null
users:
- locale: en
  notification_filter: null
  notify: true
  role: administrator
  user_id: 123456789
```

### Key Sections

* **Client Section**: Connection details for the qBittorrent server (hostname, port, username, password).
* **Redis Section**: Optional storage for runtime data (user sessions, cache, background task metadata).
* **Telegram Section**: Bot token and optional proxy settings.
* **Users Section**: Authorized Telegram users, roles, notification preferences, and locale.

---

## Client

Defines the qBittorrent client configuration.

| Name     | Type                              | Remarks                                    |
| -------- | --------------------------------- | ------------------------------------------ |
| type     | [ClientTypeEnum](#clienttypeenum) | The type of client.                        |
| host     | [HttpUrl](#httpurl)               | The IP/hostname of the qBittorrent server. |
| user     | str                               | Username for the qBittorrent server.       |
| password | str                               | Password for the qBittorrent server.       |

---

## Redis

Redis stores temporary runtime data. If omitted or `url` is `null`, an **in-memory dictionary** is used.

!!!warning
Using in-memory storage is **not recommended for production** — all data is lost when the bot restarts.
!!!

| Name | Type                  | Remarks                                               |
| ---- | --------------------- | ----------------------------------------------------- |
| url  | [RedisDsn](#redisdsn) | Redis connection string. Set `null` to disable Redis. |

---

## Telegram

Telegram bot configuration.

| Name      | Type                                              | Remarks                                  |
| --------- | ------------------------------------------------- | ---------------------------------------- |
| bot_token | str                                               | Bot token for QBittorrentBot. Required.  |
| proxy     | [TelegramProxySettings](#telegram-proxy-settings) | Optional. Proxy for Telegram connection. |

### Telegram Proxy Settings

Supports SOCKS4/5 or HTTP proxies, with optional authentication.

| Name     | Type                                          | Remarks                             |
| -------- | --------------------------------------------- | ----------------------------------- |
| scheme   | [TelegramProxyScheme](#telegram-proxy-scheme) | Protocol used for proxy connection. |
| hostname | str                                           | Proxy host address.                 |
| username | str                                           | Optional. Proxy username.           |
| password | str                                           | Optional. Proxy password.           |

---

## Users

Authorized users of QBittorrentBot.

| Name                | Type                            | Remarks                                                     |
| ------------------- | ------------------------------- | ----------------------------------------------------------- |
| user_id             | int                             | Telegram user ID.                                           |
| notify              | bool                            | Whether to notify user about new torrents.                  |
| notification_filter | list                            | List of categories to notify. Null or empty = all torrents. |
| role                | [UserRolesEnum](#userrolesenum) | Role of the user. Default: `administrator`.                 |
| locale              | str                             | User language. If not set, the language set on Telegram will be used. If not available, it will be set to English. |

---

## Enums

### ClientTypeEnum

| Name        | Type | Value         |
| ----------- | ---- | ------------- |
| QBittorrent | str  | `qbittorrent` |

### UserRolesEnum

| Name          | Type | Value           | Remarks                                                         |
| ------------- | ---- | --------------- | --------------------------------------------------------------- |
| Reader        | str  | `reader`        | Can only view torrents.                                         |
| Manager       | str  | `manager`       | Can view and manage torrents.                                   |
| Administrator | str  | `administrator` | Full access, including configuration edits and torrent removal. |

### Telegram Proxy Scheme

| Name  | Type | Value    |
| ----- | ---- | -------- |
| Sock4 | str  | `socks4` |
| Sock5 | str  | `socks5` |
| Http  | str  | `http`   |

---

## Other Types

### HttpUrl

* Accepts HTTP/HTTPS URLs.
* Requires host and TLD.
* Max length: 2083 characters.

### RedisDsn

Redis connection string example:

```
redis://[user:password]@host:port/db
```

### Languages

| Name                | Value   |
| ------------------- | ------- |
| English             | `en`    |
| Spanish             | `es`    |
| Italian             | `it`    |
| Ukrainian           | `uk`    |
| Russian             | `ru`    |
| Portuguese (Brazil) | `pt`    |

---

## Ready-to-Use `config.yml` Examples

### 1. Basic (no Redis, single user)

```yaml
client:
  type: qbittorrent
  host: http://localhost:8080/
  user: admin
  password: adminadmin

redis:
  url: null

telegram:
  bot_token: PUT_YOUR_TELEGRAM_BOT_TOKEN_HERE
  proxy: null

users:
  - user_id: 123456789
    role: administrator
    notify: true
    notification_filter: null
    locale: en
```

### 2. Docker Compose + Redis

```yaml
client:
  type: qbittorrent
  host: http://qbittorrent:8080/
  user: admin
  password: adminadmin

redis:
  url: redis://cache:6379/0

telegram:
  bot_token: PUT_YOUR_TELEGRAM_BOT_TOKEN_HERE
  proxy: null

users:
  - user_id: 123456789
    role: administrator
    notify: true
    notification_filter: null
    locale: en
```

### 3. Telegram Proxy

```yaml
client:
  type: qbittorrent
  host: http://localhost:8080/
  user: admin
  password: adminadmin

redis:
  url: null

telegram:
  bot_token: PUT_YOUR_TELEGRAM_BOT_TOKEN_HERE
  proxy:
    scheme: socks5
    hostname: 127.0.0.1
    username: proxyuser
    password: proxypass

users:
  - user_id: 123456789
    role: administrator
    notify: true
    notification_filter: null
    locale: en
```

### 4. Multi-User Setup

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

---

✅ These examples cover most common setups:

* Local testing (no Redis)
* Production with Redis and Docker
* Proxy usage
* Multiple users with custom notifications

This gives users a **plug-and-play reference** for their own `config.yml`.
