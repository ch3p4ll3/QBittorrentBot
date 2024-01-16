import uvloop
from pyrogram import Client
from pyrogram.enums.parse_mode import ParseMode
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from src.utils import torrent_finished
from ..configs import Configs


plugins = dict(
    root="src.bot.plugins"
)


proxy = None

if Configs.config.telegram.proxy is not None:
    proxy = Configs.config.telegram.proxy.proxy_settings

uvloop.install()
app = Client(
    "qbittorrent_bot",
    api_id=Configs.config.telegram.api_id,
    api_hash=Configs.config.telegram.api_hash,
    bot_token=Configs.config.telegram.bot_token,
    parse_mode=ParseMode.MARKDOWN,
    plugins=plugins,
    proxy=proxy
)

scheduler = AsyncIOScheduler()
scheduler.add_job(torrent_finished, "interval", args=[app], seconds=60)
