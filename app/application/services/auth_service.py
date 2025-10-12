from typing import Optional
from app.domain.respositories.user_repository import UserRepository
from app.application.services.jwt_service import JwtService
from app.application.services.hasher_service import HasherService
from app.domain.entities.user_entity import User as DomainUser
from app.domain.entities.auth_entity import Auth as DomainAuth


class AuthService:

    def __init__(
        self,
        user_repo: UserRepository,
        jwt_svc: JwtService,
        hasher_svc: HasherService,
    ):
        self.user_repo = user_repo
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

        access_token = self.jwt_svc.create_access_token(subject=user.id)
        refresh_token = self.jwt_svc.create_refresh_token(subject=user.id)

        return DomainAuth(access_token=access_token, refresh_token=refresh_token)

    async def verify_access(self, access_token: str) -> Optional[DomainUser]:
        """"""
        payload = self.jwt_svc.verify_access_token(token=access_token)
        sub = payload.get("sub")
        if sub:
            user: Optional[DomainUser] = await self.user_repo.get_by_id(id=sub)
            return user
        return None

    async def refresh(self, refresh_token: str) -> dict:
        pass
