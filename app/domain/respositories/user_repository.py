from abc import ABC, abstractmethod
from uuid import UUID
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.entities.user_entity import User as DomainUser


class UserRepository(ABC):

    @abstractmethod
    async def create(self, user: DomainUser, session: AsyncSession) -> DomainUser:
        """"""

    async def get_by_email(self, email: str, session: AsyncSession) -> Optional[DomainUser]:
        """"""

    @abstractmethod
    async def get_by_id(self, id: UUID, session: AsyncSession) -> Optional[DomainUser]:
        """"""

    @abstractmethod
    async def list_all(self, session: AsyncSession) -> List[DomainUser]:
        """"""

    @abstractmethod
    async def delete(self, id: UUID, session: AsyncSession) -> None:
        """"""

    @abstractmethod
    async def update(self, user: DomainUser, session: AsyncSession) -> DomainUser:
        """"""
