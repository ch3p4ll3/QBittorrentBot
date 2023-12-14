from pydantic import BaseModel
from typing import Optional


class Users(BaseModel):
    user_id: int
    notify: Optional[bool] = True
