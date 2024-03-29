import json
from enum import Enum
from typing import (
    Dict,
    List,
    Union,
)
from json import JSONDecodeError


class SameOperationEnum(Enum):
    login = 1
    swap = 2
    bridge = 3
    change = 4
    security = 5
    settings = 6
    nft = 7
    send = 8

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


class ExtractDB:

    def __new__(cls, data:  Union[Dict, List], to_list: bool = False) -> Union[Dict, List]:
        if not to_list:
            return cls.jsonb_convert(data[0]) if len(data) else dict()
        return cls.jsonb_convert(data)

    @classmethod
    def jsonb_convert(cls, data: Union[Dict, List]) -> Union[Dict, List]:
        if isinstance(data, dict):
            return cls.convert_dict(data)
        else:
            return [cls.convert_dict(item) for item in data]

    @classmethod
    def convert_dict(cls, item: dict):
        return {k: v if not cls.is_json(v) else json.loads(v) for k, v in item.items()}

    @staticmethod
    def is_json(text: str) -> bool:
        if not isinstance(text, (str, bytes, bytearray)):
            return False
        if not text:
            return False
        text = text.strip()
        if text:
            if text[0] in {'{', '['} and text[-1] in {'}', ']'}:
                try:
                    json.loads(text)
                except (ValueError, TypeError, JSONDecodeError):
                    return False
                else:
                    return True
            else:
                return False
        return False


extractDB = ExtractDB

