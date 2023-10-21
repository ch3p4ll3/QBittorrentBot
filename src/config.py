import ipaddress
from pydantic import BaseModel, field_validator
from typing import Optional
import json
from os import getenv


class Qbittorrent(BaseModel):
    ip: ipaddress.IPv4Network
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


class Telegram(BaseModel):
    bot_token: str
    api_id: int
    api_hash: str

    @field_validator('bot_token')
    def bot_token_validator(cls, v):
        if not v or not v.strip():
            raise ValueError('Bot token cannot be empty')
        return v

    @field_validator('api_hash')
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


with open(f'{ "/app/config/" if getenv("IS_DOCKER", False) else "./"}config.json', 'r') as config_json:
    BOT_CONFIGS = Main(**(json.load(config_json)))
