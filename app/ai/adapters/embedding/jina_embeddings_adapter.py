from typing import List
from langchain_community.embeddings import JinaEmbeddings
from .base_embeddings_adapter import BaseEmbeddingsAdapter


class JinaEmbeddingsAdapter(BaseEmbeddingsAdapter):

    def __init__(self, model: str, api_key: str):
        self.embed = JinaEmbeddings(jina_api_key=api_key, model_name=model)
    
    def get_embed(self) -> JinaEmbeddings:
        return self.embed

    async def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """"""
        return await self.embed.aembed_documents(texts=texts)
    
    async def embed_query(self, text: str) -> List[float]:
        """"""
        return await self.embed.aembed_query(text=text)