from typing import Optional
from pydantic import BaseModel
from .enums import TelegramProxyScheme


class TelegramProxy(BaseModel):
    scheme: TelegramProxyScheme = TelegramProxyScheme.Http  # "socks4", "socks5", "http"
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
            password=self.password  # fixed typo
        )

    @property
    def connection_string(self) -> str:
        """
        Returns the proxy connection string in the format:
        protocol://user:password@host:port
        If username/password are not provided, they are omitted.
        """
        auth = f"{self.username}:{self.password}@" if self.username and self.password else ""
        return f"{self.scheme.value}://{auth}{self.hostname}:{self.port}"
