from pydantic import BaseModel
from typing import Optional

from src.configs.enums import UserRolesEnum


class User(BaseModel):
    user_id: int
    role: UserRolesEnum = UserRolesEnum.Reader
    notify: Optional[bool] = True
