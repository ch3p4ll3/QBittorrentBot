from aiogram import Bot, Router
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.i18n import gettext as _

from src.settings import Settings
from src.settings.enums import UserRolesEnum

from src.bot.filters import HasRole
from src.bot.filters.callbacks import SettingsMenu, Menu, EditClientMenu, ReloadSettingsMenu, ToggleSpeedLimit, CheckConnection

from src.client_manager.client_repo import ClientRepo


def get_router():
    router = Router()

    @router.callback_query(SettingsMenu.filter(), HasRole(UserRolesEnum.Administrator))
    async def settings_callback(callback_query: CallbackQuery, callback_data: SettingsMenu, bot: Bot) -> None:
        await bot.edit_message_text(
            chat_id=callback_query.from_user.id,
            message_id=callback_query.message.message_id,
            text=_("QBittorrentBot Settings"),
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text=_("📥 Client Settings"), callback_data=EditClientMenu().pack())
                    ],
                    [
                        InlineKeyboardButton(text=_("🔄 Reload Settings"), callback_data=ReloadSettingsMenu().pack())
                    ],
                    [
                        InlineKeyboardButton(text=_("\uD83D\uDD19 Menu"), callback_data=Menu().pack())
                    ]
                ]
            )
        )


    @router.callback_query(EditClientMenu.filter(), HasRole(UserRolesEnum.Administrator))
    async def edit_client_settings_callback(callback_query: CallbackQuery, callback_data: EditClientMenu, bot: Bot, settings: Settings) -> None:
        repository_class = ClientRepo.get_client_manager(settings.client.type)
        speed_limit = await repository_class(settings).get_speed_limit_mode()

        speed_limit_status = _("✅ Enabled") if speed_limit else _("❌ Disabled")

        confs = _("**Speed Limit**: {speed_limit_status}"
            .format(
                speed_limit_status=speed_limit_status
            )
        )

        text = _("Edit {client_type} client settings \n\n{configs}"
            .format(
                client_type=settings.client.type.value.title(),
                configs=confs
            )
        )

        await bot.edit_message_text(
            chat_id=callback_query.from_user.id,
            message_id=callback_query.message.message_id,
            text=text,
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text=_("🐢 Toggle Speed Limit"), callback_data=ToggleSpeedLimit().pack())
                    ],
                    [
                        InlineKeyboardButton(text=_("✅ Check Client connection"), callback_data=CheckConnection().pack())
                    ],
                    [
                        InlineKeyboardButton(text=_("🔙 Settings"), callback_data=SettingsMenu().pack())
                    ]
                ]
            )
        )


    @router.callback_query(ToggleSpeedLimit.filter(), HasRole(UserRolesEnum.Administrator))
    async def toggle_speed_limit_callback(callback_query: CallbackQuery, callback_data: ToggleSpeedLimit, bot: Bot, settings: Settings) -> None:
        repository_class = ClientRepo.get_client_manager(settings.client.type)
        speed_limit = await repository_class(settings).toggle_speed_limit()

        speed_limit_status = _("✅ Enabled") if speed_limit else _("❌ Disabled")

        confs = _("**Speed Limit**: {speed_limit_status}"
            .format(
                speed_limit_status=speed_limit_status
            )
        )

        text = _("Edit {client_type} client settings \n\n{configs}"
            .format(
                client_type=settings.client.type.value.title(),
                configs=confs
            )
        )

        await bot.edit_message_text(
            chat_id=callback_query.from_user.id,
            message_id=callback_query.message.message_id,
            text=text,
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text=_("🐢 Toggle Speed Limit"), callback_data=ToggleSpeedLimit().pack())
                    ],
                    [
                        InlineKeyboardButton(text=_("✅ Check Client connection"), callback_data=CheckConnection().pack())
                    ],
                    [
                        InlineKeyboardButton(text=_("🔙 Settings"), callback_data=SettingsMenu().pack())
                    ]
                ]
            )
        )


    @router.callback_query(CheckConnection.filter(), HasRole(UserRolesEnum.Administrator))
    async def check_connection_callback(callback_query: CallbackQuery, callback_data: CheckConnection, bot: Bot, settings: Settings) -> None:
        try:
            repository_class = ClientRepo.get_client_manager(settings.client.type)
            version = await repository_class(settings).check_connection()

            await callback_query.answer(
                _(
                    "✅ The connection works. QBittorrent version: {version}"
                        .format(
                            version=version
                        )
                ), show_alert=True
            )
        except Exception:
            await callback_query.answer(_("❌ Unable to establish connection with QBittorrent"), show_alert=True)


    @router.callback_query(ReloadSettingsMenu.filter(), HasRole(UserRolesEnum.Administrator))
    async def reload_settings_callback(callback_query: CallbackQuery, callback_data: ReloadSettingsMenu, bot: Bot, settings: Settings) -> None:
        new_settings = Settings.load_settings()
        settings.update_from(new_settings)
        await callback_query.answer(_("✅ Settings Reloaded"), show_alert=True)


    return router
