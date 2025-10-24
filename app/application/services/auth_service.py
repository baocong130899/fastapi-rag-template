from datetime import datetime
from typing import AsyncIterator, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.respositories.user_repository import UserRepository
from app.domain.respositories.token_repository import TokenRepository
from app.application.services.jwt_service import JwtService
from app.application.services.hasher_service import HasherService
from app.domain.entities.user_entity import User as DomainUser
from app.domain.entities.auth_entity import (
    Auth as DomainAuth,
    AuthRefresh as DomainAuthRefresh,
)
from app.domain.entities.auth_entity import Token as DomainToken
from app.infrastructure.enums.auth_enum import TokenType


class AuthService:

    def __init__(
        self,
        user_repo: UserRepository,
        token_repo: TokenRepository,
        jwt_svc: JwtService,
        hasher_svc: HasherService,
        session_factory: AsyncIterator[AsyncSession],
    ):
        self.user_repo = user_repo
        self.token_repo = token_repo
        self.jwt_svc = jwt_svc
        self.hasher_svc = hasher_svc
        self.session_factory = session_factory

    async def login(self, email: str, password: str) -> DomainAuth:
        """"""
        async with self.session_factory() as session:

            user: Optional[DomainUser] = await self.user_repo.get_by_email(email=email, session=session)
            if user is None:
                raise Exception("Invalid credentials!.")

            # Verify password.
            is_valid = self.hasher_svc.verify_password(
                plain=password, hashed=user.hashed_password
            )
            if is_valid is not True:
                raise Exception("Invalid credentials!.")

            # Create token hash.
            user_id = user.id
            access_token = self.jwt_svc.create_access_token(subject=user_id)
            refresh_token = self.jwt_svc.create_refresh_token(subject=user_id)

            # Create access token revocation.
            access_token_payload = self.jwt_svc.get_access_token_payload()
            domain_access_token = DomainToken.create(
                user_id=user_id,
                jti=access_token_payload.get("jti"),
                type=TokenType.ACCESS.value,
                issued_at=datetime.now(),
                expires_at=access_token_payload.get("exp"),
            )
            await self.token_repo.create(token=domain_access_token, session=session)

            # Create refresh token revocation.
            refresh_token_payload = self.jwt_svc.get_refresh_token_payload()
            domain_refresh_token = DomainToken.create(
                user_id=user_id,
                jti=refresh_token_payload.get("jti"),
                type=TokenType.REFRESH.value,
                issued_at=datetime.now(),
                expires_at=refresh_token_payload.get("exp"),
            )
            await self.token_repo.create(token=domain_refresh_token, session=session)

            return DomainAuth(access_token=access_token, refresh_token=refresh_token)

    async def verify_access(self, access_token: str) -> Optional[DomainUser]:
        """"""
        async with self.session_factory() as session:

            # Check access token.
            payload = self.jwt_svc.verify_access_token(token=access_token)
            sub = payload.get("sub")
            jti = payload.get("jti")

            # Get refresh token revocation.
            record = await self.token_repo.find_by_jti(jti=jti, user_id=sub, session=session)
            if record is None:
                raise Exception("Access token not recognized!.")
            if record.revoked:
                raise Exception("Access token has been revoked!.")
             
            if sub:
                user: Optional[DomainUser] = await self.user_repo.get_by_id(id=sub, session=session)
                return user
                    
            return None

    async def refresh(self, refresh_token: str) -> DomainAuthRefresh:
        """"""
        async with self.session_factory() as session:

            # Verify refresh token.
            payload = self.jwt_svc.verify_refresh_token(token=refresh_token)
            sub = payload.get("sub")
            jti = payload.get("jti")
            if sub is None or jti is None:
                raise Exception("Invalid refresh token payload!.")
            
            # Get refresh token revocation.
            record = await self.token_repo.find_by_jti(jti=jti, user_id=sub, session=session)
            if record is None:
                raise Exception("Refresh token not recognized!.")
            if record.revoked:
                raise Exception("Refresh token has been revoked!.")
            
            # Token reuse → revoke all for user.
            if record.used:
                await self.token_repo.revoke_all_for_user(user_id=sub, session=session)
                raise Exception("Refresh token reuse detected; all tokens revoked – please re-authenticate!.")
            
            # Check user exists.
            user: Optional[DomainUser] = await self.user_repo.get_by_id(id=sub, session=session)
            if user is None:
                raise Exception("User not found!.")
            
            # Mark old refresh token as used.
            await self.token_repo.update(id=record.id, update_fields={"used": True}, session=session)
            
            # Create new access token.
            new_access_token = self.jwt_svc.create_access_token(subject=user.id)

            # Create access token revocation.
            access_token_payload = self.jwt_svc.get_access_token_payload()
            domain_access_token = DomainToken.create(
                user_id=sub,
                jti=access_token_payload.get("jti"),
                type=TokenType.ACCESS.value,
                issued_at=datetime.now(),
                expires_at=access_token_payload.get("exp"),
            )
            await self.token_repo.create(token=domain_access_token, session=session)

            return DomainAuthRefresh(access_token=new_access_token)
    
    async def revoke_token(self, user_id: str) -> bool:
        async with self.session_factory() as session:
            return await self.token_repo.revoke_all_for_user(user_id=user_id, session=session)
