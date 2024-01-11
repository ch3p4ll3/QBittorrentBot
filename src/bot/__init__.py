import uvloop
from pyrogram import Client
from pyrogram.enums.parse_mode import ParseMode
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from src.utils import torrent_finished
from ..configs import Configs


BOT_CONFIGS = Configs.config


plugins = dict(
    root="src.bot.plugins"
)


proxy = None

if BOT_CONFIGS.telegram.proxy is not None:
    proxy = BOT_CONFIGS.telegram.proxy.proxy_settings

uvloop.install()
app = Client(
    "qbittorrent_bot",
    api_id=BOT_CONFIGS.telegram.api_id,
    api_hash=BOT_CONFIGS.telegram.api_hash,
    bot_token=BOT_CONFIGS.telegram.bot_token,
    parse_mode=ParseMode.MARKDOWN,
    plugins=plugins,
    proxy=proxy
)

scheduler = AsyncIOScheduler()
scheduler.add_job(torrent_finished, "interval", args=[app], seconds=60)
