from typing import Optional
from pydantic import BaseModel, RedisDsn


class Redis(BaseModel):
    url: Optional[RedisDsn]
