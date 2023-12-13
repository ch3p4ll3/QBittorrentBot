from pyrogram import Client
from pyrogram.enums.parse_mode import ParseMode
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from src.utils import torrent_finished
from src.config import BOT_CONFIGS


plugins = dict(
    root=".plugins"
)


app = Client(
    "qbittorrent_bot",
    api_id=BOT_CONFIGS.telegram.api_id,
    api_hash=BOT_CONFIGS.telegram.api_hash,
    bot_token=BOT_CONFIGS.telegram.bot_token,
    parse_mode=ParseMode.MARKDOWN,
    plugins=plugins
)

scheduler = AsyncIOScheduler()
scheduler.add_job(torrent_finished, "interval", args=[app], seconds=60)
