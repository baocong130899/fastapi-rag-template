from typing import Any, List
from httpx import AsyncClient, Client
from langchain_openai import AzureOpenAIEmbeddings
from .base_embeddings_adapter import BaseEmbeddingsAdapter


class AzureOpenAIEmbeddingsAdapter(BaseEmbeddingsAdapter):

    def __init__(
        self,
        model: str,
        deployment: str,
        api_version: str,
        endpoint: str,
        api_key: str,
        http_async_client: AsyncClient,
        http_client: Client,
        chunk_size: int = 200,
        max_retries: int = 2,
        retry_min_seconds: int = 4,
        retry_max_seconds: int = 20,
        check_embedding_ctx_length: bool = False,
    ):
        """"""
        self.embed = AzureOpenAIEmbeddings(
            model=model,
            deployment=deployment,
            openai_api_version=api_version,
            azure_endpoint=endpoint,
            api_key=api_key,
            http_async_client=http_async_client,
            http_client=http_client,
            chunk_size=chunk_size,
            max_retries=max_retries,
            retry_min_seconds=retry_min_seconds,
            retry_max_seconds=retry_max_seconds,
            check_embedding_ctx_length=check_embedding_ctx_length,
        )

    def get_embed(self) -> AzureOpenAIEmbeddings:
        return self.embed

    async def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """"""
        return await self.embed.aembed_documents(texts=texts)
    
    async def embed_query(self, text: str) -> List[float]:
        """"""
        return await self.embed.aembed_query(text=text)