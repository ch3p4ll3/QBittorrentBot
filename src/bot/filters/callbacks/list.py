from aiogram.filters.callback_data import CallbackData


class List(CallbackData, prefix="list"):
    pass


class ListByStatus(CallbackData, prefix="by_status_list"):
    status: str | None


class Menu(CallbackData, prefix="menu"):
    pass
