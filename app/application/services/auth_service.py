from datetime import datetime
from typing import Optional
from app.domain.respositories.user_repository import UserRepository
from app.domain.respositories.refresh_token_repository import RefreshTokenRepository
from app.application.services.jwt_service import JwtService
from app.application.services.hasher_service import HasherService
from app.domain.entities.user_entity import User as DomainUser
from app.domain.entities.auth_entity import (
    Auth as DomainAuth,
    AuthRefresh as DomainAuthRefresh,
)
from app.domain.entities.auth_entity import RefreshToken as DomainRefreshToken


class AuthService:

    def __init__(
        self,
        user_repo: UserRepository,
        refresh_token_repo: RefreshTokenRepository,
        jwt_svc: JwtService,
        hasher_svc: HasherService,
    ):
        self.user_repo = user_repo
        self.refresh_token_repo = refresh_token_repo
        self.jwt_svc = jwt_svc
        self.hasher_svc = hasher_svc

    async def login(self, email: str, password: str) -> DomainAuth:
        """"""
        user: Optional[DomainUser] = await self.user_repo.get_by_email(email=email)
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

        # Create refresh token revocation.
        refresh_token_payload = self.jwt_svc.get_refresh_token_payload()
        domain_refresh_token = DomainRefreshToken.create(
            user_id=user_id,
            jti=refresh_token_payload.get("jti"),
            token_hash=refresh_token,
            issued_at=datetime.now(),
            expires_at=refresh_token_payload.get("exp"),
        )
        await self.refresh_token_repo.create(refresh_token=domain_refresh_token)

        return DomainAuth(access_token=access_token, refresh_token=refresh_token)

    async def verify_access(self, access_token: str) -> Optional[DomainUser]:
        """"""
        payload = self.jwt_svc.verify_access_token(token=access_token)
        sub = payload.get("sub")
        if sub:
            user: Optional[DomainUser] = await self.user_repo.get_by_id(id=sub)
            return user
        return None

    async def refresh(self, refresh_token: str) -> DomainAuthRefresh:
        """"""
        # Verify refresh token.
        payload = self.jwt_svc.verify_refresh_token(token=refresh_token)
        sub = payload.get("sub")
        jti = payload.get("jti")
        if sub is None or jti is None:
            raise Exception("Invalid refresh token payload!.")
        
        # Get refresh token revocation.
        record = await self.refresh_token_repo.find_by_jti(jti=jti, user_id=sub)
        if record is None:
            raise Exception("Refresh token not recognized!.")
        if record.revoked:
            raise Exception("Refresh token has been revoked!.")
        
        # Token reuse → revoke all for user.
        if record.used:
            await self.refresh_token_repo.update(model=record, update_fields={"used": True})
            raise Exception("Refresh token reuse detected; all tokens revoked – please re-authenticate!.")
        
        # Check user exists.
        user: Optional[DomainUser] = await self.user_repo.get_by_id(id=sub)
        if user is None:
            raise Exception("User not found!.")
        
        # Create new access token.
        new_access_token = self.jwt_svc.create_access_token(subject=user.id)

        return DomainAuthRefresh(access_token=new_access_token)
    
    async def revoke_token(self, user_id: str) -> None:
        async with self.async_session as session:
            update_stmt = update(RefreshTokenModel).where(
                RefreshTokenModel.user_id == user_id
            ).values(revoked=True, revoked_at=datetime.utcnow())
            await session.execute(update_stmt)
            await session.commit()
        

        

