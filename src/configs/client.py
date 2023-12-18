from pydantic import BaseModel, field_validator, IPvAnyAddress
from .enums import ClientTypeEnum


class Client(BaseModel):
    type: ClientTypeEnum = ClientTypeEnum.QBittorrent
    host: IPvAnyAddress
    port: int
    user: str
    password: str

    @field_validator('port')
    def port_validator(cls, v):
        if v <= 0:
            raise ValueError('Port must be >= 0')
        return v

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
    def parsed_host(self) -> str:
        return f"http://{self.host}"

    @property
    def full_host_string(self) -> str:
        return f"{self.parsed_host}:{self.port}"

    @property
    def connection_string(self) -> dict:
        if self.type is ClientTypeEnum.QBittorrent:
            return dict(
                host=self.full_host_string,
                username=self.user,
                password=self.password
            )
