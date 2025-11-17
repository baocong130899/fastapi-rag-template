from enum import Enum
from typing import List


class FileExtensionEnum(Enum):
    """"""

    PDF = "pdf"
    TXT = "txt"

    @classmethod
    def has_value(cls, value: str) -> bool:
        """"""
        return value.lower() in (item.value for item in cls)
    
    @classmethod
    def get_values(cls) -> List[str]:
        values = []
        for item in cls:
            values.extend(item.value)

        return values