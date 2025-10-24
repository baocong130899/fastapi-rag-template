from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from app.domain.entities.auth_entity import RefreshToken as DomainRefreshToken
from app.infrastructure.models.auth_model import RefreshTokenModel


class RefreshTokenRepository(ABC):

    @abstractmethod
    async def create(self, refresh_token: DomainRefreshToken) -> DomainRefreshToken:
        """"""

    @abstractmethod
    async def find_by_jti(self, jti: str, user_id: str) -> Optional[DomainRefreshToken]:
        """"""

    @abstractmethod
    async def update(self, model: RefreshTokenModel, update_fields: Dict[str, Any]) -> DomainRefreshToken:
        """"""

    @abstractmethod
    async def revoke_all_for_user(self, user_id: int) -> bool:
        """"""