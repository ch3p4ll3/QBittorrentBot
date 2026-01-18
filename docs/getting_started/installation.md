---
label: Installation-Updating
---

# Installation

To start using the bot, you must first create a directory that will contain **Docker Compose**, configuration files, logs, and runtime data.

We recommend using a dedicated project directory.

Example:

```
/home/user/docker/QBittorrentBot
```

This directory will be the **project root** for the bot.

---

## Recommended directory structure

Inside the project directory, use the following structure:

```
QBittorrentBot/
├── docker-compose.yml
└── data/
    ├── config.yml
    └── logs/
```

**Explanation:**

* `docker-compose.yml`
  Located in the project root. All start, stop, and update commands must be executed from this directory.

* `data/`
  Persisted storage mounted into the container as `/app/data`.
  This directory contains:

  * `config.yml` – bot configuration
  * `logs/` – application logs

---

## Configuration file

The bot configuration is stored in:

```
data/config.yml
```

You may create this file **before or after** starting the bot.

* If `config.yml` exists, the bot will load it at startup.
* If it does not exist, the bot will **automatically generate a default `config.yml`** inside the `data/` directory on first launch.

After the initial generation, you must edit the file and **restart the bot once** to apply the initial configuration.

### Configuration migration

If a configuration file from a previous version (`config.json`) is found in the `data/` directory, the bot will:

1. Automatically remove the old `config.json`
2. Create a new `config.yml` using the current configuration format

---

### Automatic configuration reload

QBittorrentBot automatically reloads the configuration file whenever a change is detected.
Most configuration updates take effect **without restarting the bot**.

!!!warning Warning
Changes to the **Telegram bot token** require a **full bot restart** to take effect.
!!!

For detailed configuration options, see:
[Configuration File](configuration_file.md)

---

## Start the bot

Create a file named `docker-compose.yml` **in the project root directory** (`QBittorrentBot/`) with the following content:

```
services:
  bot:
    image: "ch3p4ll3/qbittorrent-bot:latest"
    container_name: qbittorrent-bot
    restart: unless-stopped
    depends_on:
      - cache
    volumes:
      - "./data:/app/data"

  cache:
    image: redis:8
    container_name: redis-cache
    restart: unless-stopped
```

From the same directory (where `docker-compose.yml` is located), start the bot:

```
docker compose up -d
```

---

# Updating

To update QBittorrentBot to the latest version, navigate to the **project root directory** and run:

```
docker compose pull
docker compose up -d
```

Docker Compose will download the new image and restart the containers automatically.

---


Here’s a polished version of your **“Running without Docker”** section that includes instructions for running with **UV** and makes everything clearer and more structured:

---

# Running without Docker

Using Docker is **strongly recommended**, as it isolates the application from the host system and avoids dependency-related issues.

If Docker cannot be used, you can run the bot directly in two ways: **standard Python mode** or **UV mode**.

+++ Standard Python
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
   pip3 install -r pyproject.toml
   ```

4. Create or generate a `config.yml` file.

5. Start the bot:

   ```bash
   python3 -m src.main
   ```

+++ UV
**UV** is a modern Python environment manager that can simplify dependency and project management.

1. Install UV by following the [official guide](https://docs.astral.sh/uv/).

2. Clone the repository (if not already done):

   ```bash
   git clone https://github.com/ch3p4ll3/QBittorrentBot.git
   cd QBittorrentBot
   ```

3. Install dependencies via UV:

   ```bash
   uv sync
   ```

4. Start the bot:

   ```bash
   uv run python -m src.main
   ```

> ✅ Advantages of using UV:
>
> * Automatic dependency isolation
> * Easier environment management
> * Cross-platform reproducibility

+++

---

### ⚠️ Notes

When running **without Docker**, you are responsible for:

* Ensuring the correct **Python version** is installed
* Managing dependencies manually (unless using UV)
* Setting up **Redis** if you plan to use it
* Supervising the bot process (e.g., with `systemd`)
