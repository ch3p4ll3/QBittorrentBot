from aiogram import Bot, Router
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.i18n import gettext as _

from src.client_manager.client_repo import ClientRepo
from src.settings import Settings, User
from src.settings.enums import UserRolesEnum
from src.redis_helper.wrapper import RedisWrapper

from src.bot.filters import HasRole
from src.bot.filters.callbacks import AddCategory, SelectCategory, CategoryMenu, Menu, RemoveCategory, ModifyCategory, CategoryAction, AddMagnet, AddTorrent


def get_router():
    router = Router()

    @router.callback_query(CategoryMenu.filter(), HasRole(UserRolesEnum.Administrator))
    async def menu_category_callback(callback_query: CallbackQuery, callback_data: CategoryMenu, bot: Bot) -> None:
        await bot.edit_message_text(
            chat_id=callback_query.from_user.id,
            message_id=callback_query.message.message_id,
            text=_("Pause/Resume a download"),
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text=_("➕ Add Category"), callback_data=AddCategory().pack()),
                    ],
                    [
                        InlineKeyboardButton(text=_("🗑 Remove Category"), callback_data=SelectCategory(action="remove_category").pack())
                    ],
                    [
                        InlineKeyboardButton(text=_("📝 Modify Category"), callback_data=SelectCategory(action="modify_category").pack())],
                    [
                        InlineKeyboardButton(text=_("\uD83D\uDD19 Menu"), callback_data=Menu().pack())
                    ]
                ]
            )
        )

    @router.callback_query(AddCategory.filter(), HasRole(UserRolesEnum.Administrator))
    @router.callback_query(AddCategory.filter(), HasRole(UserRolesEnum.Manager))
    async def add_category_callback(callback_query: CallbackQuery, bot: Bot, redis: RedisWrapper) -> None:
        await redis.set(f"action:{callback_query.from_user.id}", "category_name")
        button = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text=_("\uD83D\uDD19 Menu"), callback_data=Menu().pack())
                ]
            ]
        )

        try:
            await bot.edit_message_text(
                chat_id=callback_query.from_user.id,
                message_id=callback_query.message.message_id,
                text=_("Send the category name"),
                reply_markup=button
            )

        except Exception:
            await bot.send_message(
                callback_query.from_user.id,
                _("Send the category name"),
                reply_markup=button
            )


    @router.callback_query(SelectCategory.filter(), HasRole(UserRolesEnum.Administrator))
    @router.callback_query(SelectCategory.filter(), HasRole(UserRolesEnum.Manager))
    async def list_categories(callback_query: CallbackQuery, callback_data: SelectCategory, bot: Bot, settings: Settings):
        buttons = []

        repository_class_class = ClientRepo.get_client_manager(settings.client.type)
        categories = repository_class_class(settings).get_categories()

        if categories is None:
            buttons.append([InlineKeyboardButton(text=_("\uD83D\uDD19 Menu"), callback_data=Menu().pack())])

            await bot.edit_message_text(
                chat_id=callback_query.from_user.id,
                message_id=callback_query.message.message_id,
                text=_("There are no categories"),
                reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
            )

            return

        for _, i in enumerate(categories):
            buttons.append([InlineKeyboardButton(text=i, callback_data=f"{callback_data.action}:{i}")])

        buttons.append([InlineKeyboardButton(text=_("\uD83D\uDD19 Menu"), callback_data=Menu().pack())])

        try:
            await bot.edit_message_text(
                chat_id=callback_query.from_user.id,
                message_id=callback_query.message.message_id,
                text=_("Choose a category:"),
                reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
            )

        except Exception:
            await bot.send_message(
                callback_query.from_user.id,
                _("Choose a category:"),
                reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
            )


    @router.callback_query(RemoveCategory.filter(), HasRole(UserRolesEnum.Administrator))
    async def remove_category_callback(callback_query: CallbackQuery, callback_data: RemoveCategory, bot: Bot, settings: Settings) -> None:
        buttons = [
            [
                InlineKeyboardButton(text=_("\uD83D\uDD19 Menu"), callback_data=Menu().pack())
            ]
        ]

        repository_class = ClientRepo.get_client_manager(settings.client.type)
        await repository_class(settings).remove_category(callback_data.category)

        await bot.edit_message_text(
            chat_id=callback_query.from_user.id,
            message_id=callback_query.message.message_id,
            text=_("The category {category_name} has been removed"
                .format(
                    category_name=callback_data.category
                )
            ),
            reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
        )


    @router.callback_query(ModifyCategory.filter(), HasRole(UserRolesEnum.Administrator))
    async def modify_category_callback(callback_query: CallbackQuery, callback_data: ModifyCategory, bot: Bot, redis: RedisWrapper) -> None:
        buttons = [
            [
                InlineKeyboardButton(text=_("\uD83D\uDD19 Menu"), callback_data=Menu().pack())
            ]
        ]

        await redis.set(f"action:{callback_query.from_user.id}", f"category_dir_modify#{callback_data.category}")

        await bot.edit_message_text(
            chat_id=callback_query.from_user.id,
            message_id=callback_query.message.message_id,
            text=_("Send new path for category {category_name}"
                .format(
                    category_name=callback_data.category
                )
            ),
            reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
        )


    @router.callback_query(CategoryAction.filter(), HasRole(UserRolesEnum.Administrator))
    @router.callback_query(CategoryAction.filter(), HasRole(UserRolesEnum.Manager))
    async def category(callback_query: CallbackQuery, callback_data: CategoryAction, bot: Bot, settings: Settings) -> None:
        buttons = []

        repository_class = ClientRepo.get_client_manager(settings.client.type)
        categories = await repository_class(settings).get_categories()
        callback_type = AddMagnet if callback_data.action.startswith('add_magnet') else AddTorrent

        for i in categories:
            buttons.append([InlineKeyboardButton(text=i, callback_data=callback_type(category=i).pack())])

        buttons.append([InlineKeyboardButton(text="None", callback_data=callback_type(category=None).pack())])
        buttons.append([InlineKeyboardButton(text=_("\uD83D\uDD19 Menu"), callback_data=Menu().pack())])

        try:
            await bot.edit_message_text(
                chat_id=callback_query.from_user.id,
                message_id=callback_query.message.message_id,
                text=_("Choose a category:"),
                reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
            )

        except Exception:
            await bot.send_message(
                callback_query.from_user.id,
                _("Choose a category:"),
                reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
            )

    return router
