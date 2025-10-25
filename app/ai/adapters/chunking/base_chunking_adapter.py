from abc import ABC, abstractmethod
from typing import Sequence
from langchain_core.documents import Document


class BaseChunkingAdapter(ABC):
    

    @abstractmethod
    async def atransform_documents(self, documents: Sequence[Document])-> Sequence[Document]:
        """"""