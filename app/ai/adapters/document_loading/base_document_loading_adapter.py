from abc import ABC, abstractmethod
from typing import List
from langchain_core.documents import Document


class BaseDocumentLoadingAdapter(ABC):

    @abstractmethod
    async def load(self, file_path: str) -> List[Document]:
        """"""