from src.bot import app, scheduler
import logging
from logging import handlers
from src.configs import Configs
from os.path import exists
from os import mkdir


if not exists(Configs.log_folder):
    mkdir(Configs.log_folder)

# Create a file handler
handler = handlers.TimedRotatingFileHandler(
    f'{Configs.log_folder}/QbittorrentBot.log',
    when='midnight',
    backupCount=10
)

# Create a format
formatter = logging.Formatter(Configs.config.logger.format)
handler.setFormatter(formatter)

logging.getLogger().addHandler(handler)

# Set logging level to DEBUG
logging.getLogger().setLevel(Configs.config.logger.parsed_level)

if __name__ == '__main__':
    scheduler.start()
    print("Bot started")
    app.run()
