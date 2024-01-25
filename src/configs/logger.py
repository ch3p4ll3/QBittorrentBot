from pydantic import BaseModel
from .enums import LoggerEnum
from logging import getLevelNamesMapping, WARNING


class Logger(BaseModel):
    level: LoggerEnum = LoggerEnum.WARNING
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    @property
    def parsed_level(self):
        mapping = getLevelNamesMapping()

        return mapping.get(self.level.value, WARNING)
