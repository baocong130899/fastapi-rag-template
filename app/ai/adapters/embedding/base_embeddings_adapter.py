from abc import ABC, abstractmethod
from typing import List
from langchain_core.embeddings import Embeddings

class BaseEmbeddingsAdapter(ABC):

    @abstractmethod
    def get_embed(self) -> Embeddings:
        """"""

    @abstractmethod
    async def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """"""
    
    @abstractmethod
    async def embed_query(self, text: str) -> List[float]:
        """"""