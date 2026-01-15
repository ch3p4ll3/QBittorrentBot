from aiogram import Bot, Router
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from settings import Settings
from settings.user import User
from settings.enums import UserRolesEnum
from translator import Translator, Strings

from ....filters import HasRole
from ....filters.callbacks import SettingsMenu, Menu, EditClientMenu, ReloadSettingsMenu, ToggleSpeedLimit, CheckConnection

from redis_helper.wrapper import RedisWrapper
from client_manager import ClientRepo


def get_router():
    router = Router()

    @router.callback_query(SettingsMenu.filter(), HasRole(UserRolesEnum.Administrator))
    async def settings_callback(callback_query: CallbackQuery, callback_data: SettingsMenu, bot: Bot, user: User) -> None:
        await bot.edit_message_text(
            chat_id=callback_query.from_user.id,
            message_id=callback_query.message.message_id,
            text=Translator.translate(Strings.Menu, user.locale),
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text=Translator.translate(Strings.ClientSettings, user.locale), callback_data=EditClientMenu().pack())
                    ],
                    [
                        InlineKeyboardButton(text=Translator.translate(Strings.ReloadSettings, user.locale), callback_data=ReloadSettingsMenu().pack())
                    ],
                    [
                        InlineKeyboardButton(text=Translator.translate(Strings.BackToMenu, user.locale), callback_data=Menu().pack())
                    ]
                ]
            )
        )


    @router.callback_query(EditClientMenu.filter(), HasRole(UserRolesEnum.Administrator))
    async def edit_client_settings_callback(callback_query: CallbackQuery, callback_data: EditClientMenu, bot: Bot, settings: Settings, user: User) -> None:
        repository_class = ClientRepo.get_client_manager(settings.client.type)
        speed_limit = repository_class(settings).get_speed_limit_mode()

        speed_limit_status = Translator.translate(Strings.Enabled if speed_limit else Strings.Disabled, user.locale)

        confs = Translator.translate(
            Strings.SpeedLimitStatus,
            user.locale,
            speed_limit_status=speed_limit_status
        )

        await bot.edit_message_text(
            chat_id=callback_query.from_user.id,
            message_id=callback_query.message.message_id,
            text=Translator.translate(Strings.EditClientSettings, user.locale, client_type=settings.client.type, configs=confs),
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text=Translator.translate(Strings.ToggleSpeedLimit, user.locale), callback_data=ToggleSpeedLimit().pack())
                    ],
                    [
                        InlineKeyboardButton(text=Translator.translate(Strings.CheckClientConnection, user.locale), callback_data=CheckConnection().pack())
                    ],
                    [
                        InlineKeyboardButton(text=Translator.translate(Strings.BackToSettings, user.locale), callback_data=SettingsMenu().pack())
                    ]
                ]
            )
        )


    @router.callback_query(ToggleSpeedLimit.filter(), HasRole(UserRolesEnum.Administrator))
    async def toggle_speed_limit_callback(callback_query: CallbackQuery, callback_data: ToggleSpeedLimit, bot: Bot, settings: Settings, user: User) -> None:
        repository_class = ClientRepo.get_client_manager(settings.client.type)
        speed_limit = repository_class(settings).toggle_speed_limit()

        speed_limit_status = Translator.translate(Strings.Enabled if speed_limit else Strings.Disabled, user.locale)

        confs = Translator.translate(
            Strings.SpeedLimitStatus,
            user.locale,
            speed_limit_status=speed_limit_status
        )

        speed_limit_status = Translator.translate(Strings.Enabled if speed_limit else Strings.Disabled, user.locale)

        confs = Translator.translate(
            Strings.SpeedLimitStatus,
            user.locale,
            speed_limit_status=speed_limit_status
        )

        await bot.edit_message_text(
            chat_id=callback_query.from_user.id,
            message_id=callback_query.message.message_id,
            text=Translator.translate(Strings.EditClientSettings, user.locale, client_type=settings.client.type, configs=confs),
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text=Translator.translate(Strings.ToggleSpeedLimit, user.locale), callback_data=ToggleSpeedLimit().pack())
                    ],
                    [
                        InlineKeyboardButton(text=Translator.translate(Strings.CheckClientConnection, user.locale), callback_data=CheckConnection().pack())
                    ],
                    [
                        InlineKeyboardButton(text=Translator.translate(Strings.BackToSettings, user.locale), callback_data=SettingsMenu().pack())
                    ]
                ]
            )
        )


    @router.callback_query(CheckConnection.filter(), HasRole(UserRolesEnum.Administrator))
    async def check_connection_callback(callback_query: CallbackQuery, callback_data: CheckConnection, bot: Bot, settings: Settings, user: User) -> None:
        try:
            repository_class = ClientRepo.get_client_manager(settings.client.type)
            version = repository_class(settings).check_connection()

            await callback_query.answer(Translator.translate(Strings.ClientConnectionOk, user.locale, version=version), show_alert=True)
        except Exception:
            await callback_query.answer(Translator.translate(Strings.ClientConnectionBad, user.locale), show_alert=True)


    @router.callback_query(ReloadSettingsMenu.filter(), HasRole(UserRolesEnum.Administrator))
    async def reload_settings_callback(callback_query: CallbackQuery, callback_data: ReloadSettingsMenu, bot: Bot, settings: Settings, user: User) -> None:
        new_settings = Settings.load_settings()
        settings.update_from(new_settings)
        await callback_query.answer(Translator.translate(Strings.SettingsReloaded, user.locale), show_alert=True)


    return router
