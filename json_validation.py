from typing import List
from pydantic import BaseModel
import json


class Qbittorrent(BaseModel):
    ip: str
    port: str
    user: str
    password: str


class Validator(BaseModel):
    token: str
    qbittorrent: Qbittorrent
    id: List[int] = []


def get_configs():
    with open("login.json") as login_file:
        validator = Validator(**json.load(login_file))
        return validator
