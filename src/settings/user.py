from pydantic import BaseModel
from typing import Optional, List

from src.settings.enums import UserRolesEnum


class User(BaseModel):
    user_id: int
    role: UserRolesEnum = UserRolesEnum.Reader
    locale: Optional[str] = "en"
    notify: Optional[bool] = True
    notification_filter: Optional[List[str]] = None  # leave empty if or None for disabling notify filter, set a category name to receive notifications for specific categories
