from abc import ABC, abstractmethod
from typing import List, Iterable
from langchain_core.vectorstores import VectorStore


class BaseVectorStoreAdapter(ABC):

    @abstractmethod
    async def load(self) -> VectorStore:
        """"""

    @abstractmethod
    async def aadd_embeddings(
        self,
        texts: Iterable[str],
        embeddings: List[List[float]],
        metadatas: List[dict] | None = None,
        ids: List[str] | None = None,
        **kwargs: List,
    ) -> List[str]:
        """"""