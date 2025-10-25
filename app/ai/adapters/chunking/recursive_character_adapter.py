from typing import List, Sequence
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from app.ai.adapters.chunking.base_chunking_adapter import BaseChunkingAdapter


class RecursiveCharacterAdapter(BaseChunkingAdapter):
    """"""
    def __init__(
        self, 
        chunk_size: int,
        chunk_overlap: int,
        separators: List[str],
    ):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            is_separator_regex=False,
            separators=separators,
        )
    
    async def atransform_documents(self, documents: Sequence[Document])-> Sequence[Document]:
        return self.text_splitter.atransform_documents(documents=documents)