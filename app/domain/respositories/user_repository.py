from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.user_entity import User as DomainUser


class UserRepository(ABC):

    @abstractmethod
    async def create(self, user: DomainUser) -> DomainUser:
        """"""

    async def get_by_email(self, email: str) -> Optional[DomainUser]:
        """"""

    @abstractmethod
    async def get_by_id(self, id: str) -> Optional[DomainUser]:
        """"""

    @abstractmethod
    async def list_all(self) -> List[DomainUser]:
        """"""

    @abstractmethod
    async def delete(self, id: str) -> bool:
        """"""

    @abstractmethod
    async def update(self, user: DomainUser) -> DomainUser:
        """"""
