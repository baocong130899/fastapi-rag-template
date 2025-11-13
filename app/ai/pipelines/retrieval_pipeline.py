from app.ai.adapters.embedding import Embedder
from app.ai.adapters.vectorstore import VectorStore

class RetrievalPipeline:
    
    def __init__(
        self,
        embedder: Embedder,
        vector_store: VectorStore
    ):
        """"""
        self.embedder = embedder
        self.vector_store = vector_store

    async def retrieve(self):
        """"""