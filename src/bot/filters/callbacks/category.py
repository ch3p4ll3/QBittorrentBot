from aiogram.filters.callback_data import CallbackData


class CategoryMenu(CallbackData, prefix="menu_categories"):
    pass


class AddCategory(CallbackData, prefix="add_category"):
    pass


class SelectCategory(CallbackData, prefix="select_category"):
    action: str


class RemoveCategory(CallbackData, prefix="remove_category"):
    category: str


class ModifyCategory(CallbackData, prefix="modify_category"):
    category: str


class CategoryAction(CallbackData, prefix="category"):
    action: str
