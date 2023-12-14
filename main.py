from src.bot import app, scheduler
import logging
from logging import handlers
from os import getenv

# Create a file handler
handler = logging.handlers.TimedRotatingFileHandler(
    f'{"/app/config/" if getenv("IS_DOCKER", False) else "./"}logs/QbittorrentBot.log',
    when='midnight',
    backupCount=10
)

# Create a format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logging.getLogger().addHandler(handler)
# Set logging level to DEBUG
logging.getLogger().setLevel(logging.DEBUG)

if __name__ == '__main__':
    scheduler.start()
    print("Bot started")
    app.run()
