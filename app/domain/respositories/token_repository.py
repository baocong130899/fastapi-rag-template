from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.entities.auth_entity import Token as DomainToken
from app.infrastructure.models.auth_model import TokenModel


class TokenRepository(ABC):

    @abstractmethod
    async def create(self, token: DomainToken, session: AsyncSession) -> DomainToken:
        """"""

    @abstractmethod
    async def find_by_jti(self, jti: str, user_id: str, session: AsyncSession) -> Optional[DomainToken]:
        """"""

    @abstractmethod
    async def update(self, id: str, update_fields: Dict[str, Any], session: AsyncSession) -> Optional[int]:
        """"""
    
    @abstractmethod
    async def revoke_by_jti(self, jti: str, user_id: str, session: AsyncSession) -> Optional[DomainToken]:
        """"""

    @abstractmethod
    async def revoke_all_for_user(self, user_id: str, session: AsyncSession) -> bool:
        """"""