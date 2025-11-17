import os
from typing import List
from fastapi import UploadFile
import filetype


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
        
    def __check_mime_type(self, mime: str):
        """"""
        if mime not in self.allowed_mime_types:
            raise ValueError(f"Unsupported mime type: {mime}.")
    
    def __check_file_size(self, size: int):
        """"""
        if size == 0:
            raise ValueError("Uploaded file is empty.")
        
        if size > self.max_file_size:
            raise ValueError(f"Too large: {self.max_file_size} KB.")
    
    async def __check_extension(self, file: UploadFile):
        """"""
        _, ext = os.path.splitext(file.filename.lower())
        if ext not in self.allowed_extensions:
            raise ValueError(f"Unsupported extension: {ext}.")

        data = await file.read(1024)
        file.file.seek(0)
        kind = filetype.guess(data)
        if kind is None or kind.extension not in self.allowed_extensions:
            raise ValueError("Uploaded file content doesn’t match allowed types.")

    async def validate(self, file: UploadFile):
        """"""
        self.__check_file_size(size=file.size)
        await self.__check_extension(file=file)
        self.__check_mime_type(mime=file.content_type)
        
        
    