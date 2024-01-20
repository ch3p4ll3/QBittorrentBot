from typing import Optional
from pydantic import BaseModel
from .enums import TelegramProxyScheme


class TelegramProxy(BaseModel):
    scheme: TelegramProxyScheme = TelegramProxyScheme.Http  # "socks4", "socks5" and "http" are supported
    hostname: str
    port: int
    username: Optional[str] = None
    password: Optional[str] = None

    @property
    def proxy_settings(self):
        return dict(
            scheme=self.scheme.value,
            hostname=self.hostname,
            port=self.port,
            username=self.username,
            passowrd=self.password
        )
