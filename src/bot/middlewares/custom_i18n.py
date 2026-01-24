from __future__ import annotations

from typing import TYPE_CHECKING, Any

from aiogram.utils.i18n.middleware import I18nMiddleware

try:
    from babel import Locale, UnknownLocaleError
except ImportError:  # pragma: no cover
    Locale = None  # type: ignore

    class UnknownLocaleError(Exception):  # type: ignore
        pass


if TYPE_CHECKING:
    from aiogram.types import TelegramObject, User as AiogramUser
    from aiogram.utils.i18n.core import I18n
    from src.settings.user import User


class CustomI18nMiddleware(I18nMiddleware):
    """
    Custom I18n middleware based on SimpleI18nMiddleware.

    Chooses language code from the User settings, if not specified uses the User locale received in event.
    """

    def __init__(
        self,
        i18n: I18n,
        i18n_key: str | None = "i18n",
        middleware_key: str = "i18n_middleware",
    ) -> None:
        super().__init__(i18n=i18n, i18n_key=i18n_key, middleware_key=middleware_key)

        if Locale is None:  # pragma: no cover
            msg = (
                f"{type(self).__name__} can be used only when Babel installed\n"
                "Just install Babel (`pip install Babel`) "
                "or aiogram with i18n support (`pip install aiogram[i18n]`)"
            )
            raise RuntimeError(msg)

    async def get_locale(self, event: TelegramObject, data: dict[str, Any]) -> str:
        if Locale is None:  # pragma: no cover
            msg = (
                f"{type(self).__name__} can be used only when Babel installed\n"
                "Just install Babel (`pip install Babel`) "
                "or aiogram with i18n support (`pip install aiogram[i18n]`)"
            )
            raise RuntimeError(msg)

        user: User | None = data.get("user")
        event_from_user: AiogramUser | None = data.get("event_from_user")

        if user is not None and user.locale is not None:
            if user.locale not in self.i18n.available_locales:
                return self.i18n.default_locale
            return user.locale

        if event_from_user is None or event_from_user.language_code is None:
            return self.i18n.default_locale
        try:
            locale = Locale.parse(event_from_user.language_code, sep="-")
        except UnknownLocaleError:
            return self.i18n.default_locale

        if locale.language not in self.i18n.available_locales:
            return self.i18n.default_locale
        return locale.language
