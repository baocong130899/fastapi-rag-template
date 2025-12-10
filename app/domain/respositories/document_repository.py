from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.entities import DomainDocument


class DocumentRepository(ABC):   

    @abstractmethod
    async def create(self, domain: DomainDocument, session: AsyncSession) -> DomainDocument:
        """"""
