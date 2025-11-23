from enum import Enum
from typing import List


class DocumentUploadMimeType(Enum):
    PDF = ["application/pdf"]
    TEXT = ["text/plain"]
    # DOC = [
    #     "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    #     "application/msword",
    # ]
    # HTML = ["text/html"]
    @classmethod
    def get_values(cls) -> List[str]:
        values = []
        for item in cls:
            values.extend(item.value)

        return values