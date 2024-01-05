from dataclasses import dataclass
from typing import Union


@dataclass
class Torrent:
    hash: str
    name: str
    progress: int
    dlspeed: int
    state: str
    size: int
    eta: int
    category: Union[str, None]
