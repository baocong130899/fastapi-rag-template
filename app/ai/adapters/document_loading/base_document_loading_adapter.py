from abc import ABC, abstractmethod
from langchain_community.document_loaders.base import BaseLoader


class BaseDocumentLoadingAdapter(ABC):

    @abstractmethod
    async def load(self) -> BaseLoader:
        """"""