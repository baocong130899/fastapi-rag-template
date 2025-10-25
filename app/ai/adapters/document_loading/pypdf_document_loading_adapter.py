from typing import List
from langchain_community.document_loaders.base import BaseLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from app.ai.adapters.document_loading.base_document_loading_adapter import BaseDocumentLoadingAdapter


class PyPDFDocumentLoadingAdapter(BaseDocumentLoadingAdapter):

    def __init__(self, mode: str):
        """"""
        self.mode = mode
    
    def __loader(self, file_path: str) -> BaseLoader:
        """"""
        return PyPDFLoader(file_path=file_path, mode=self.mode)

    async def load(self, file_path: str) -> List[Document]:
        """"""
        loader = self.__loader(file_path=file_path)

        return await loader.aload()