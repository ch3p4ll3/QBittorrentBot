import ipaddress
from pydantic import BaseModel, validator
from typing import Optional
import json


class Qbittorrent(BaseModel):
    ip: ipaddress.IPv4Network
    port: int
    user: str
    password: str

    @validator('port')
    def port_validator(cls, v):
        if v <= 0:
            raise ValueError('Port must be >= 0')
        return v

    @validator('user')
    def user_validator(cls, v):
        if not v or not v.strip():
            raise ValueError('User cannot be empty')
        return v

    @validator('password')
    def password_validator(cls, v):
        if not v or not v.strip():
            raise ValueError('Password cannot be empty')
        return v


class Telegram(BaseModel):
    bot_token: str
    api_id: int
    api_hash: str

    @validator('bot_token')
    def bot_token_validator(cls, v):
        if not v or not v.strip():
            raise ValueError('Bot token cannot be empty')
        return v

    @validator('api_hash')
    def api_hash_validator(cls, v):
        if not v or not v.strip():
            raise ValueError('API HASH cannot be empty')
        return v


class Users(BaseModel):
    user_id: int
    notify: Optional[bool] = True


class Main(BaseModel):
    qbittorrent: Qbittorrent
    telegram: Telegram
    users: list[Users]


with open('/app/config/config.json', 'r') as config_json:
    BOT_CONFIGS = Main(**(json.load(config_json)))
