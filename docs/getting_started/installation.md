---
label: Installation-Updating
---

# Installation

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
+++

# Updating

+++ Docker
To update to the latest version of QBittorrentBot, use the following commands to stop then remove the old version:
- `docker stop qbittorrent-bot`
- `docker rm qbittorrent-bot`

Now that you have stopped and removed the old version of QBittorrentBot, you must ensure that you have the latest version of the image locally. You can do this with a docker pull command:

`docker pull ch3p4ll3/qbittorrent-bot:latest`

Finally, deploy the updated version of Portainer:

`docker run -d -v /home/user/docker/QBittorrentBot:/app/config:rw --name qbittorrent-bot ch3p4ll3/qbittorrent-bot:latest`
+++ Docker compose
To update to the latest version of QBittorrentBot, navigate to the folder where you created the `docker-compose.yml` file.

Then use the following command to pull the latest version of the image:

`docker compose pull`

Finally use the following command to start the bot using Docker Compose:
`docker compose up -d`
+++

# Running without docker
it is preferable to use the bot using docker, this gives the developers to isolate their app from its environment, solving the “it works on my machine” headache.

In case you could not use docker you can use the bot without it. To do so, follow the following steps:
- Clone this repo `git clone https://github.com/ch3p4ll3/QBittorrentBot.git`
- Move in the project directory
- Install dependencies with `pip3 install -r requirements.txt`
- Create a config.json file
- Start the bot with `python3 main.py`