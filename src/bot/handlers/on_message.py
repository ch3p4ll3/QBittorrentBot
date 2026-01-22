import logging
import tempfile

from aiogram import F
from aiogram import Bot
from aiogram.types import Message
from aiogram.dispatcher.router import Router
from aiogram.fsm.context import FSMContext

from src.client_manager.client_repo import ClientRepo
from src.settings import Settings
from src.settings.user import User
from src.bot.filters import IsAuthorizedUser, IsCommand
from src.translator import Translator, Strings
from src.bot.fsm import AddMagnetForm, AddTorrent, AddCategory, EditCategory

from .common import send_menu


logger = logging.getLogger(__name__)


def get_router():
    router = Router()

    @router.message(~F.from_user.is_bot, ~IsCommand(), IsAuthorizedUser(), AddMagnetForm.send_magnets)
    async def on_magnet(message: Message, user: User, state: FSMContext, bot: Bot, settings: Settings):
        if message.text.startswith("magnet:?xt"):
            magnet_link = message.text.split("\n")

            category = (await state.get_data())['select_category']

            repository_class = ClientRepo.get_client_manager(settings.client.type)
            response = await repository_class(settings).add_magnet(
                magnet_link=magnet_link,
                category=category
            )

            if not response:
                await message.reply(Translator.translate(Strings.UnableToAddMagnet, locale=user.locale))
                return

            await send_menu(bot, state, settings, message.chat.id, message.message_id)
            await state.clear()

        else:
            await message.reply(
                Translator.translate(Strings.InvalidMagnet, locale=user.locale)
            )


    @router.message(~F.from_user.is_bot, ~IsCommand(), IsAuthorizedUser(), AddTorrent.send_torrent)
    async def on_torrent(message: Message, user: User, state: FSMContext, bot: Bot, settings: Settings):
        if ".torrent" in message.document.file_name:
            with tempfile.TemporaryDirectory() as tempdir:
                name = f"{tempdir}/{message.document.file_name}"
                category = (await state.get_data())['select_category']

                file = await bot.get_file(message.document.file_id)
                file_path = file.file_path
                await bot.download_file(file_path, name)

                repository_class = ClientRepo.get_client_manager(settings.client.type)
                response = await repository_class(settings).add_torrent(file_name=name, category=category)

                if not response:
                    await message.reply(Translator.translate(Strings.UnableToAddTorrent, locale=user.locale))
                    return

            await send_menu(bot, state, settings, message.chat.id, message.message_id)
            await state.clear()

        else:
            await message.reply(
                Translator.translate(Strings.InvalidTorrent, locale=user.locale)
            )


    @router.message(~F.from_user.is_bot, ~IsCommand(), IsAuthorizedUser(), AddCategory.category_name)
    async def on_category_name(message: Message, state: FSMContext):
        await state.update_data(name=message.text)
        await state.set_state(AddCategory.category_directory)

        await message.reply(
            Translator.translate(Strings.CategoryPath, category_name=message.text)
        )


    @router.message(~F.from_user.is_bot, ~IsCommand(), IsAuthorizedUser(), AddCategory.category_directory)
    async def on_category_create(message: Message, state: FSMContext, bot: Bot, settings: Settings):
        category_name = (await state.get_data())['category_name']

        repository_class = ClientRepo.get_client_manager(settings.client.type)

        await repository_class(settings).create_category(name=category_name, save_path=message.text.replace("\\", ""))
        await send_menu(bot, state, settings, message.chat.id, message.message_id)
        await state.clear()


    @router.message(~F.from_user.is_bot, ~IsCommand(), IsAuthorizedUser(), EditCategory.category_directory)
    async def on_category_edit(message: Message, state: FSMContext, bot: Bot, settings: Settings):
        category_name = (await state.get_data())['category_name']

        repository_class = ClientRepo.get_client_manager(settings.client.type)

        await repository_class(settings).edit_category(name=category_name, save_path=message.text.replace("\\", ""))
        await send_menu(bot, state, settings, message.chat.id, message.message_id)
        await state.clear()

    return router
