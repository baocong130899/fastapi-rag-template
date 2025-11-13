from typing import List
from langchain_community.embeddings import JinaEmbeddings


class JinaEmbeddingsAdapter():
    """"""
    def __init__(self, jina_api_key: str, model_name: str):
        self.text_embeddings = JinaEmbeddings(
            jina_api_key=jina_api_key, model_name=model_name
        )
    
    async def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """"""
        return await self.text_embeddings.aembed_documents(texts=texts)