# Getting Started

In order to start using the bot, you must first create a folder where the bot will fish for settings and where it will save logs

For example: let's create a folder called `QBittorrentBot` in the home of the user `user`. The path to the folder will then be `/home/user/docker/QBittorrentBot`.

Before starting the bot you need to place the configuration file in this folder. You can rename the `config.json.template` file to `config.json` and change the parameters as desired. Go [here](configuration_file.md) to read more about the configuration file.

Once that is done you can start the bot using docker, you can use either docker or docker compose.

+++ Docker
Open your terminal and execute the following command to start the bot container:

`docker run -d -v /home/user/docker/QBittorrentBot:/app/config:rw --name qbittorrent-bot ch3p4ll3/qbittorrent-bot:latest`
+++ Docker compose
Create a file named `docker-compose.yml` inside a directory with the following content:
```
version: '3.9'
services:
    qbittorrent-bot:
        image: 'ch3p4ll3/qbittorrent-bot:latest'
        container_name: qbittorrent-bot
        restart: unless-stopped
        volumes:
            - '/home/user/docker/QBittorrentBot:/app/config:rw'
```

Run the following command to start the bot using Docker Compose:
`docker compose up -d`