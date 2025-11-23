import os
from typing import List
from fastapi import UploadFile
import filetype
from app.ai.enums import FileExtensionProvider


class DocumentUploadValidator:

    def __init__(
        self, 
        max_file_size: int,
        allowed_extensions: List[str],
        allowed_mime_types: List[str],
    ):
        self.max_file_size = max_file_size
        self.allowed_extensions = allowed_extensions
        self.allowed_mime_types = allowed_mime_types
        
    def __check_file_size(self, size: int):
        """"""
        if size == 0:
            raise ValueError("Uploaded file is empty.")
        
        if size > self.max_file_size:
            raise ValueError(f"Too large: {self.max_file_size} KB.")
    
    async def __check_filetype(self, file: UploadFile):
        """"""
        ext = os.path.splitext(file.filename.lower())[1][1:]
        if ext not in self.allowed_extensions:
            raise ValueError(f"Unsupported extension: {ext}.")

        data = await file.read(1024)
        file.file.seek(0)
        kind = filetype.guess(data)

        if kind is None and ext == FileExtensionProvider.TXT.value:
            return
        
        if kind is None or kind.mime not in self.allowed_mime_types:
            raise ValueError("Uploaded file content doesn’t match allowed types.")

    async def validate(self, file: UploadFile):
        """"""
        self.__check_file_size(size=file.size)
        await self.__check_filetype(file=file)
        
        
    