from aiogram.fsm.state import State, StatesGroup


class AddMagnetForm(StatesGroup):
    select_category = State()
    send_magnets = State()


class AddTorrent(StatesGroup):
    select_category = State()
    send_torrent = State()


class AddCategory(StatesGroup):
    category_name = State()
    category_directory = State()

class EditCategory(StatesGroup):
    category_name = State()
    category_directory = State()
