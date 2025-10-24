from datetime import datetime
from typing import Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.domain.respositories.token_repository import TokenRepository
from app.domain.entities.auth_entity import Token as DomainToken
from app.infrastructure.models.auth_model import TokenModel


class SqlAlchemyTokenRepository(TokenRepository):
     
    async def create(self, token: DomainToken, session: AsyncSession) -> DomainToken:
        """"""
        new_model = TokenModel(
            user_id=token.user_id,
            jti=token.jti,
            type=token.type,
            issued_at=token.issued_at,
            expires_at=token.expires_at,
            used=token.used,
            revoked=token.revoked,
            revoked_at=token.revoked_at
        )
        session.add(new_model)
        await session.commit()
        await session.refresh(new_model)
        
        return DomainToken(
            id=str(new_model.id),
            user_id=str(new_model.user_id),
            jti=new_model.jti,
            type=token.type,
            issued_at=new_model.issued_at,
            expires_at=new_model.expires_at,
            used=new_model.used,
            revoked=new_model.revoked,
            revoked_at=new_model.revoked_at,
        ) 
        
    async def find_by_jti(self, jti: str, user_id: str, session: AsyncSession) -> Optional[DomainToken]:
        """"""
        stmt = select(TokenModel).where(
            TokenModel.jti == jti,
            TokenModel.user_id == user_id
        )
        result = await session.execute(stmt)
        model = result.scalar_one_or_none()

        if model:
            return DomainToken(
                id=str(model.id),
                user_id=str(model.user_id),
                jti=model.jti,
                type=model.type,
                issued_at=model.issued_at,
                expires_at=model.expires_at,
                used=model.used,
                revoked=model.revoked,
                revoked_at=model.revoked_at,
            )  

    async def update(self, id: str, update_fields: Dict[str, Any], session: AsyncSession) -> Optional[int]:
        """"""
        stmt = (
            update(TokenModel)
            .where(
                TokenModel.id == id,
            )
            .values(**update_fields)
            .execution_options(synchronize_session="fetch")
        )
        result = await session.execute(stmt)
        await session.commit()
        return result.rowcount
    
    async def revoke_by_jti(self, jti: str, user_id: str, session: AsyncSession) -> bool:
        """"""
        stmt = update(TokenModel).where(
            TokenModel.user_id == user_id,
            TokenModel.jti == jti,
            TokenModel.revoked == False
        ).values(
            revoked=True,
            revoked_at=datetime.now()
        )
        await session.execute(stmt)
        await session.commit()

        return True

    async def revoke_all_for_user(self, user_id: str, session: AsyncSession) -> bool:
        """"""
        stmt = update(TokenModel).where(
            TokenModel.user_id == user_id,
            TokenModel.revoked == False
        ).values(
            revoked=True,
            revoked_at=datetime.now()
        )
        await session.execute(stmt)
        await session.commit()

        return True
