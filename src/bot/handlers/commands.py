from aiogram import Bot
from aiogram.types import Message
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.dispatcher.router import Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

import psutil

from src.redis_helper.wrapper import RedisWrapper
from src.utils import convert_size
from src.settings import User, Settings
from src.translator import Translator, Strings

from ..filters import IsAuthorizedUser
from .common import send_menu


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


    @router.message(CommandStart(), IsAuthorizedUser())
    async def start_command(message: Message, state: FSMContext, bot: Bot, settings: Settings) -> None:
        """Start the bot."""
        await state.clear()
        await send_menu(bot, state, settings, message.chat.id, message.message_id)


    @router.message(Command("stats"), IsAuthorizedUser())
    async def stats_command(message: Message, user: User) -> None:
        try:
            cpu_temp = psutil.sensors_temperatures()['coretemp'][0].current
        except KeyError:
            cpu_temp = 0

        stats_text = Translator.translate(
            Strings.StatsCommand,
            user.locale,
            cpu_usage=psutil.cpu_percent(interval=None),
            cpu_temp=cpu_temp,
            free_memory=convert_size(psutil.virtual_memory().available),
            total_memory=convert_size(psutil.virtual_memory().total),
            memory_percent=psutil.virtual_memory().percent,
            disk_used=convert_size(psutil.disk_usage('/mnt').used),
            disk_total=convert_size(psutil.disk_usage('/mnt').total),
            disk_percent=psutil.disk_usage('/mnt').percent
        )

        await message.reply(stats_text)

    return router
