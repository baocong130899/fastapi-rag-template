from app.ai.adapters.document_loading import DocumentLoader
from app.ai.adapters.chunking import TextSplitter
from app.ai.adapters.embedding import Embedder
from app.ai.adapters.vectorstore import VectorStore
from app.ai.factories import LoaderFactory

class IndexingPipeline:
    
    def __init__(
        self,
        loader_factory: LoaderFactory,
        text_splitter: TextSplitter,
        embedder: Embedder,
        vector_store: VectorStore
    ):
        """"""
        self.loader_factory = loader_factory
        self.text_splitter = text_splitter
        self.embedder = embedder
        self.vector_store = vector_store

    async def ingest(self, file_path: str):
        """"""
        # Document loading.
        # document_loader = self.loader_factory.get(file_path=file_path)
        # documents = await document_loader.load(file_path=file_path)

        # chunks = await self.text_splitter.atransform_documents(documents=documents)

        # embeddings = await self.embedder.embed_documents()





