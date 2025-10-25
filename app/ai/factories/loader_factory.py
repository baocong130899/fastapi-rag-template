import os
from langchain_community.document_loaders.base import BaseLoader
from app.ai.adapters.document_loading import BaseDocumentLoadingAdapter
from app.ai.enums import FileExtensionProvider


class LoaderFactoryWrapper:

    def __init__(self, factory_aggregate):
        self.factory_aggregate = factory_aggregate
    
    def check_extension(self, file_path: str) -> FileExtensionProvider:
        """"""
        ext = os.path.splitext(file_path)[1].lower().strip(".")
        if not FileExtensionProvider.has_value(ext):
            raise ValueError(f"Unsupported file extension: .{ext}")
        return FileExtensionProvider(ext)

    async def load(self, file_path: str) -> BaseLoader:
        """"""
        ext = self.check_extension(file_path).value
        loader: BaseDocumentLoadingAdapter = self.factory_aggregate[ext]()
        return await loader.load(file_path)
