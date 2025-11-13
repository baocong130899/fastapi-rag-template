from typing import Optional, Iterable, List
from langchain_postgres import PGVectorStore, PGEngine
from langchain_core.embeddings import Embeddings
from sqlalchemy.ext.asyncio import AsyncEngine
from .base_vectorstore_adapter import BaseVectorStoreAdapter


class PostgresVectorStoreAdapter(BaseVectorStoreAdapter):

    def __init__(self, embeddings_function: Embeddings, engine: AsyncEngine):
        """"""
        self.embedding_service = embeddings_function
        self.pg_engine = PGEngine.from_engine(engine=engine)
        self.table_name = "embeddings"
        self.schema_name = "public"
        self.content_column = "content"
        self.embedding_column = "embed"
        self.metadata_columns = ["document_id"]
        self.id_column = "id"
        self.metadata_json_column = "cmetadata"
        self.hybrid_search_config = None
        self._store: Optional[PGVectorStore] = None

    async def load(self) -> PGVectorStore:
        """"""
        if self._store is not None:
            return self._store
        
        self._store: PGVectorStore = await PGVectorStore.create(
            engine=self.pg_engine,
            embedding_service=self.embedding_service,
            table_name=self.table_name,
            id_column=self.id_column,
            metadata_json_column=self.metadata_json_column,
            embedding_column=self.embedding_column,
            content_column=self.content_column,
            metadata_columns=self.metadata_columns
        )
        return self._store
    
    async def aadd_embeddings(
        self,
        texts: Iterable[str],
        embeddings: List[List[float]],
        metadatas: List[dict] | None = None,
        ids: List[str] | None = None,
        **kwargs: List,
    ) -> List[str]:
        vs = await self.load()
        return await vs.aadd_embeddings(texts=texts, embeddings=embeddings, metadatas=metadatas, ids=ids, **kwargs)