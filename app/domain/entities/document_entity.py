from dataclasses import dataclass
from uuid import UUID
from datetime import datetime
from typing import Optional


@dataclass
class Document:
    id: Optional[UUID]
    user_id: UUID
    file_name: str
    content_type: str
    file_size: float
    file_hash: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def create(
        cls,
        user_id: UUID,
        file_name: str,
        content_type: str,
        file_size: float,
        file_hash: str,
    ) -> "Document":
        return cls(
            id=None,
            user_id=user_id,
            file_name=file_name,
            content_type=content_type,
            file_size=file_size,
            file_hash=file_hash,
        )
