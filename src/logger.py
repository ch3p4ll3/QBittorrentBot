from logging import config
from os.path import exists
from os import mkdir


def configure_logger(base_path):
    path = base_path
    for i in ['data', 'logs']:
        path = path / i
        if not exists(path):
            mkdir(path)

    # Logging configuration dictionary
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            },
            "detailed": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "DEBUG",
                "formatter": "default",
            },
            "file": {
                "class": "logging.handlers.TimedRotatingFileHandler",
                "level": "DEBUG",
                "formatter": "detailed",
                "filename": base_path / 'data/logs/QbittorrentBot.log',
                "when": "midnight",
                "interval": 1,
                "backupCount": 7,
                "encoding": "utf-8",
            },
        },
        "loggers": {
            "watchfiles.main": {
                "level": "WARNING",  # Suppress DEBUG logs for watchfiles.main
                "handlers": ["console"],  # Optionally include this for higher-level messages
                "propagate": False,
            },
        },
        "root": {
            "level": "DEBUG",
            "handlers": ["console", "file"],
        },
    }

    # Apply logging configuration
    config.dictConfig(logging_config)
