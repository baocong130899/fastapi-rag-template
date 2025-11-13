import os
from app.ai.adapters.document_loading import DocumentLoader
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

    def get(self, file_path: str) -> DocumentLoader:
        """"""
        ext = self.check_extension(file_path).value
        return self.factory_aggregate[ext]()
