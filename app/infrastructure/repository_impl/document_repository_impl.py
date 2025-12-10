from uuid import UUID
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.domain.respositories import DocumentRepository
from app.domain.entities import DomainDocument
from app.infrastructure.models import DocumentModel


class SQLAlchemyDocumentRepository(DocumentRepository):
    """Class representing a person"""

    async def create(self, domain: DomainDocument, session: AsyncSession) -> DomainDocument:
        """"""
        document_model = DocumentModel(
            user_id=domain.user_id,
            file_name=domain.file_name,
            content_type=domain.content_type,
            file_size=domain.file_size,
            file_hash=domain.file_hash,
        )
        session.add(document_model)
        await session.commit()
        await session.refresh(document_model)

        domain.id = document_model.id
        domain.created_at = document_model.created_at
        domain.updated_at = document_model.updated_at

        return domain

        