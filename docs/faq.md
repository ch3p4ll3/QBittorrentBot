---
order: -20
---

# FAQ

### What is QBittorrentBot?

**QBittorrentBot** is a Telegram bot that allows you to control your qBittorrent downloads directly from within Telegram. It enables users to add torrents, manage downloads, monitor progress, and interact with the torrent client—all through simple commands in a Telegram chat.

### What are the benefits of using QBittorrentBot?

Using **QBittorrentBot** provides several advantages:

* **Remote Control:** Manage your torrents without having to open the qBittorrent client. Control your downloads from anywhere, at any time.
* **Efficiency:** Save time by accessing all torrent management functions from within Telegram.
* **Organized Management:** Categorize and filter torrents for better accessibility and ease of use.
* **Docker Support:** Easily deploy and manage the bot via Docker, ensuring a smooth and scalable experience.

### How do I add QBittorrentBot to my Telegram account?

To start using **QBittorrentBot**, follow this guide:
[!ref Getting Started](getting_started)

### How do I edit the configuration for QBittorrentBot?

The bot’s configuration is stored in a **`config.yml`** file (replacing the previous **`config.json`** format). This file contains all the necessary details such as qBittorrent connection settings, Telegram bot token, user roles, and Redis settings. To edit it:

1. Open **`config.yml`** in any text editor.
2. Adjust the fields according to your setup.
3. Save the file and restart the bot.

For detailed information about configuration options, refer to the [configuration guide](./getting_started/configuration_file.md).

### How do I check the status of my torrents?

To check the status of your torrents, use the **list torrents** command within the bot. This will display all active torrents along with essential details like:

* Torrent name
* Current status
* Progress
* Download/upload speed

### What is the difference between a magnet link and a torrent file?

* **Magnet Link:** A Magnet link is a URI (Uniform Resource Identifier) that points to torrent metadata, allowing you to download a file without needing the .torrent file. It's often more convenient and lightweight.
* **Torrent File:** A .torrent file contains metadata about a specific torrent, such as file sizes, structure, and trackers. It must be downloaded first before you can use it in a torrent client.

### What are the different user roles available in QBittorrentBot?

**QBittorrentBot** supports three user roles, each with varying permissions:

* **Reader:** Can view active torrents and details but cannot modify them.
* **Manager:** In addition to Reader permissions, can manage torrent settings (pause, resume, set priority), add/edit categories, etc.
* **Administrator:** Has full control, including all Manager privileges, removing torrents, editing configurations, and managing users.

### How do I change a user's role?

You can change a user's role by modifying the **`config.yml`** file:

1. Open the **`config.yml`**.
2. Find the user entry you want to modify under the **`users`** section.
3. Change the `role` field to one of the following: `reader`, `manager`, or `administrator`.
4. Save the file. If you're an admin, you can also **reload the configuration** from the bot itself to apply the changes without restarting.

### How do I install QBittorrentBot on my server?

The recommended method to install **QBittorrentBot** is via Docker, which ensures a seamless and isolated environment for the bot.

1. Install **Docker** on your server.
2. Clone the repository and configure your **`config.yml`**.
3. Run the bot using the provided Docker setup.

If you prefer running without Docker, you can follow the manual setup guide [here](./getting_started/installation.md#running-without-docker).

### How do I add a new manager to my QBittorrentBot?

To add a new manager:

1. Edit the **`config.yml`** file.
2. Add a new user under the `users` section, specifying their **`role`** as `manager` and their **`user_id`**.
3. Reload the bot configuration or restart the bot to apply the changes.

For a detailed guide, follow [this tutorial](advanced/add_new_client_manager.md).

### How do I add a new entry to the QBittorrentBot configuration file?

To add new settings (e.g., a new Telegram bot, additional clients, etc.):

1. Open **`config.yml`**.
2. Add the new entries under the appropriate sections.
3. Save the file and reload the configuration in the bot (if running) or restart the bot.

For more information, see [Adding new entries in the configuration](advanced/add_entries_configuration.md).

### How do I contribute to the development of QBittorrentBot?

QBittorrentBot is open-source! You can contribute by:

* Reporting bugs
* Suggesting improvements
* Submitting pull requests

To get involved, check out the project's [GitHub repository](https://github.com/ch3p4ll3/QBittorrentBot).
For contribution guidelines, please refer to the [Contributing Guide](contributing.md).
