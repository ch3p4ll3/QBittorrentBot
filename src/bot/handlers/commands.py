from aiogram import F
from aiogram import Bot
from aiogram.types import Message
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.dispatcher.router import Router
from aiogram.filters import CommandStart, Command

import psutil

from ..custom_filters import IsAuthorizedUser
from redis_helper.wrapper import RedisWrapper
from utils import convert_size, inject_user
from .common import send_menu
from settings import User, Settings
from translator import Translator, Strings


def get_router():
    router = Router()

    @router.message(~IsAuthorizedUser())
    async def access_denied_message(message: Message) -> None:
        buttons = [
            [
                InlineKeyboardButton(
                    text="Github",
                    url="https://github.com/ch3p4ll3/QBittorrentBot/"
                )
            ]
        ]

        markup = InlineKeyboardMarkup(inline_keyboard=buttons)

        await message.reply("You are not authorized to use this bot", reply_markup=markup)


    @router.message(Command("start"), IsAuthorizedUser())
    async def start_command(message: Message, redis: RedisWrapper, bot: Bot, settings: Settings) -> None:
        """Start the bot."""
        await redis.set(f"action:{message.from_user.id}", None)
        await send_menu(bot, redis, settings, message.chat.id, message.message_id)


    @router.message(Command("stats"), IsAuthorizedUser())
    @inject_user
    async def stats_command(message: Message, user: User) -> None:
        stats_text = Translator.translate(
            Strings.StatsCommand,
            user.locale,
            cpu_usage=psutil.cpu_percent(interval=None),
            cpu_temp=psutil.sensors_temperatures()['coretemp'][0].current,
            free_memory=convert_size(psutil.virtual_memory().available),
            total_memory=convert_size(psutil.virtual_memory().total),
            memory_percent=psutil.virtual_memory().percent,
            disk_used=convert_size(psutil.disk_usage('/mnt').used),
            disk_total=convert_size(psutil.disk_usage('/mnt').total),
            disk_percent=psutil.disk_usage('/mnt').percent
        )

        await message.reply(stats_text)

    return router