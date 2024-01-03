import json
from pathlib import Path
from typing import Dict
from string import Template
from ..utils import get_value


def load_locales(locales_path: Path) -> Dict:
    # check if format is supported
    # get list of files with specific extensions
    data = {}

    for file in locales_path.glob("*.json"):
        # get the name of the file without extension, will be used as locale name
        locale = file.stem
        with open(file, 'r', encoding='utf8') as f:
            data[locale] = json.load(f)

    return data


class Translator:
    locales: Dict = load_locales(Path(__file__).parent.parent / 'locales')

    @classmethod
    def translate(cls, key, locale: str = 'en', **kwargs) -> str:
        # return the key instead of translation text if locale is not supported
        if locale not in cls.locales:
            return key

        text = get_value(cls.locales[locale], key)

        return Template(text).safe_substitute(**kwargs)

    @classmethod
    def reload_locales(cls) -> Dict:
        cls.locales = load_locales(Path(__file__).parent.parent / 'locales')

        return cls.locales
