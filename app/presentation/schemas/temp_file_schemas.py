from pydantic import BaseModel


class TempFile(BaseModel):
    file_name: str
    file_size: float
    content_type: str
    dest_path: str
    hexdigest: str