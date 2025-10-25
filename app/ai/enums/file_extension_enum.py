from enum import Enum


class FileExtensionProvider(Enum):
    """"""

    PDF = "pdf"
    TXT = "txt"

    @classmethod
    def has_value(cls, value: str) -> bool:
        """"""
        return value.lower() in (item.value for item in cls)