from aiogram.filters.callback_data import CallbackData


class PauseResumeMenu(CallbackData, prefix="menu_pause_resume"):
    pass


class Pause(CallbackData, prefix="pause"):
    torrent_hash: str


class Resume(CallbackData, prefix="resume"):
    torrent_hash: str


class PauseAll(CallbackData, prefix="pause_all"):
    pass


class ResumeAll(CallbackData, prefix="resume_all"):
    pass
