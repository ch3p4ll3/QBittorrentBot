---
order: -20
---
# FAQ

### What is QBittorrentBot?

QBittorrentBot is a Telegram bot that allows you to control your qBittorrent downloads from within the Telegram app. It can add torrents, manage your torrent list, and much more.

### What are the benefits of using QBittorrentBot?

There are several benefits to using QBittorrentBot, including:

* **Convenience:** You can control your torrents from anywhere, without having to open the qBittorrent app.
* **Efficiency:** You can manage your torrents without switching between apps.
* **Organization:** You can categorize your torrents for better organization and accessibility.
* **Docker Support:** You can deploy and manage the bot seamlessly using Docker containers.

### How do I add QBittorrentBot to my Telegram account?

Follow this guide to start using QBittorrentBot
[!ref Getting Started](getting_started)

### How do I edit the configuration for the QBittorrentBot?

The QBittorrentBot configuration file is located at config.json. This file stores the bot's settings, such as the connection details for the qBittorrent client, the API IDs and hashes, and the list of authorized users. To edit the configuration file, you can open it in a text editor and make the necessary changes.

### How do I check the status of my torrents?

You can check the status of your torrents by using the list torrents button. This command will display a list of all your active torrents, including their name, status, progress, and download/upload speed.

### What is the difference between a magnet link and a torrent file?

A magnet link is a URI scheme that allows you to download a torrent without having to download the entire torrent file. A torrent file is a file that contains metadata about the torrent, such as the filename, file size, and number of pieces.

### What are the different user roles available in QBittorrentBot?

QBittorrentBot supports three user roles: Reader, Manager, and Admin. Each role has different permissions, as follows:

* **Reader:** Can view lists of active torrents and view individual torrent details.
* **Manager:** Can perform all Reader actions, plus add/edit categories, set torrent priorities, and pause/resume downloads.
* **Admin:** Can perform all Manager actions, plus remove torrents, remove categories, and edit configs.

### How do I change the user role for a user?

You can change the user role for a user by editing the `config.json` file. Open the file and find the user's entry. Change the `role` field to the desired role (e.g., "reader", "manager", or "admin"). Save the file and restart the bot or, if you are an admin you can reload the configuration from the bot.

### How do I install QBittorrentBot on my server?

You can install QBittorrentBot on your server using Docker. First, install Docker on your server. Then, create a Docker image from the QBittorrentBot Dockerfile. Finally, run the Docker image to start the bot.

### How do I add a new manager to my QBittorrentBot?

Please follow this guide
[!ref Add new client manager](advanced/add_new_client_manager)

### How do I add a new entry to the QBittorrentBot configuration file?

Please follow this guide
[!ref Add new entries in configuration file](advanced/add_entries_configuration)

### How do I contribute to the development of QBittorrentBot?

QBittorrentBot is an open-source project. You can contribute to the development by reporting bugs, suggesting improvements, or submitting pull requests. The project's code is hosted on [GitHub](https://github.com/ch3p4ll3/QBittorrentBot).