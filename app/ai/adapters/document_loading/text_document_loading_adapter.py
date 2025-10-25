from typing import List
from langchain_community.document_loaders.base import BaseLoader
from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document
from app.ai.adapters.document_loading.base_document_loading_adapter import BaseDocumentLoadingAdapter


class TextDocumentLoadingAdapter(BaseDocumentLoadingAdapter):
    
    def __loader(self, file_path: str) -> BaseLoader:
        """"""
        return TextLoader(file_path=file_path)

    async def load(self, file_path: str) -> List[Document]:
        """"""
        loader = self.__loader(file_path=file_path)

        return await loader.aload()