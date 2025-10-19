from datetime import datetime
from typing import AsyncIterator, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.domain.respositories.refresh_token_repository import RefreshTokenRepository
from app.domain.entities.auth_entity import RefreshToken as DomainRefreshToken
from app.infrastructure.models.auth_model import RefreshTokenModel


class SqlAlchemyRefreshTokenRepository(RefreshTokenRepository):
     
    def __init__(self, session_factory: AsyncIterator[AsyncSession]):
        self.session_factory = session_factory

    async def create(self, refresh_token: DomainRefreshToken) -> DomainRefreshToken:
        """"""
        async with self.session_factory() as session:
            session: AsyncSession

            new_model = RefreshTokenModel(
                user_id=refresh_token.user_id,
                jti=refresh_token.jti,
                token_hash=refresh_token.token_hash,
                issued_at=refresh_token.issued_at,
                expires_at=refresh_token.expires_at,
                used=refresh_token.used,
                revoked=refresh_token.revoked,
                revoked_at=refresh_token.revoked_at
            )
            session.add(new_model)
            await session.commit()
            await session.refresh(new_model)
            
            return DomainRefreshToken(
                user_id=str(new_model.user_id),
                jti=new_model.jti,
                token_hash=new_model.token_hash,
                issued_at=new_model.issued_at,
                expires_at=new_model.expires_at,
                used=new_model.used,
                revoked=new_model.revoked,
                revoked_at=new_model.revoked_at,
            ) 
        
    async def find_by_jti(self, jti: str, user_id: str) -> Optional[DomainRefreshToken]:
        """"""
        async with self.session_factory() as session:
            session: AsyncSession

            stmt = select(RefreshTokenModel).where(
                RefreshTokenModel.jti == jti,
                RefreshTokenModel.user_id == user_id
            )
            result = await session.execute(stmt)
            model = result.scalar_one_or_none()

            if model:
                return DomainRefreshToken(
                    user_id=str(model.user_id),
                    jti=model.jti,
                    token_hash=model.token_hash,
                    issued_at=model.issued_at,
                    expires_at=model.expires_at,
                    used=model.used,
                    revoked=model.revoked,
                    revoked_at=model.revoked_at,
                )  

    async def update(self, model: RefreshTokenModel, update_fields: Dict[str, Any]) -> DomainRefreshToken:
        """"""
        async with self.session_factory() as session:
            session: AsyncSession

            for field_name, value in update_fields.items():
                if hasattr(model, field_name):
                    setattr(model, field_name, value)
                else:
                    raise ValueError(f"Field '{field_name}' does not exist on RefreshTokenModel!.")
            
            await session.commit()
            await session.refresh(model)
            
            return DomainRefreshToken(
                user_id=str(model.user_id),
                jti=model.jti,
                token_hash=model.token_hash,
                issued_at=model.issued_at,
                expires_at=model.expires_at,
                used=model.used,
                revoked=model.revoked,
                revoked_at=model.revoked_at,
            )  

    async def revoke_all_for_user(self, user_id: int) -> bool:
        """"""
        async with self.session_factory() as session:
            session: AsyncSession

            stmt = update(RefreshTokenModel).where(
                RefreshTokenModel.user_id == user_id,
                RefreshTokenModel.revoked == False
            ).values(
                revoked=True,
                revoked_at=datetime.now()
            )
            await session.execute(stmt)
            await session.commit()

            return True
