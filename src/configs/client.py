from pydantic import BaseModel, field_validator, HttpUrl
from .enums import ClientTypeEnum


class Client(BaseModel):
    type: ClientTypeEnum = ClientTypeEnum.QBittorrent
    host: HttpUrl
    user: str
    password: str

    @field_validator('user')
    def user_validator(cls, v):
        if not v or not v.strip():
            raise ValueError('User cannot be empty')
        return v

    @field_validator('password')
    def password_validator(cls, v):
        if not v or not v.strip():
            raise ValueError('Password cannot be empty')
        return v

    @property
    def qbittorrent_connection_string(self) -> dict:
        if self.type is ClientTypeEnum.QBittorrent:
            return dict(
                host=self.host.unicode_string(),
                username=self.user,
                password=self.password
            )

    @property
    def transmission_connection_string(self) -> dict:
        if self.type is ClientTypeEnum.QBittorrent:
            return dict(
                host=self.host.host,
                port=self.host.port,
                username=self.user,
                password=self.password
            )

