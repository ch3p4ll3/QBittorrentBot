---
order: -15
---
# RSS management

Administrators can manage qBittorrent's RSS downloader from Telegram: add feeds, and create rules that download new uploads automatically. Only users with the `administrator` role can use it, and feed URLs are never printed back in the chat because they often contain passkeys.

## With buttons

Open `/start` and tap **📡 RSS**, or send `/rss`.

* **👀 Watch for a name**: pick a feed, send the words to wait for (for example `Foo Show 1080p`), pick a category, then say whether it is a TV show. A new upload whose title contains all the words is downloaded automatically.
  Everything the feed already holds is marked as read first, so only uploads that appear from now on are downloaded. If the feed cannot be refreshed or marked (a slow or unreachable feed), the bot tells you and older matching uploads may be downloaded too.
* **📡 Feeds / 📋 Rules**: tap an item to enable, disable or remove it (removal asks for confirmation).
* **➕ Add feed**: send `name url`. Your message is deleted right away because it contains the feed URL.

### TV shows

The TV options are **opt-in**: they are only applied when you answer "Yes, a TV show" in the button flow, or add `show` as the last field of `/rss_addrule`. No category name is treated specially. For a TV show rule:

* qBittorrent's **smart episode filter** is turned on, so an episode that was already downloaded (for example a re-release) is not downloaded again.
* If the category has a save path, the downloads go into a **folder named after the show** inside it (for example `Shows/Foo Show`). The category is matched against qBittorrent's real category list, ignoring case.

!!!warning
An explicit save path switches qBittorrent's automatic torrent management off for that rule.
!!!

## With commands

| Command | What it does |
|---|---|
| `/rss` | Open the RSS button menu (same as `/start` and RSS) |
| `/rss_list` | Show feeds (host only) and download rules as text |
| `/rss_addfeed <name> <url>` | Add a feed. Your message is deleted right away |
| `/rss_delfeed <name>` | Remove a feed |
| `/rss_addrule <name> ; <feed or all> ; <must contain> ; [must not contain] ; [category] ; [show]` | Add and enable a rule |
| `/rss_delrule <name>` | Remove a rule |
| `/rss_toggle <name>` | Enable or disable a rule |
| `/rss_help` | Show this help in the chat |

The fields of `/rss_addrule` are separated by a semicolon (`;`). A `|` inside a field is kept as it is: qBittorrent reads it as "or" in the must-contain field.

Example, a TV show with the smart filter and a show folder:

```
/rss_addrule Foo Show ; myfeed ; Foo 1080p ; 720p ; TV ; show
```

The bot lists the RSS commands in the Telegram `/` menu only for administrators.
