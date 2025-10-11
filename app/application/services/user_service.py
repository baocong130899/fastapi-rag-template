from app.domain.respositories.user_repository import UserRepository
from app.domain.entities.user_entity import User as DomainUser
from app.application.services.hasher_service import HasherService


class UserService:

    def __init__(
        self,
        user_repo: UserRepository,
        hasher_svc: HasherService,
    ):
        self.user_repo = user_repo
        self.hasher_svc = hasher_svc

    async def create_user(
        self, email: str, name: str, is_active: bool, password: str
    ) -> DomainUser:
        user = DomainUser.create(
            hasher_svc=self.hasher_svc,
            email=email,
            name=name,
            is_active=is_active,
            password=password,
        )
        return await self.user_repo.create(user=user)
