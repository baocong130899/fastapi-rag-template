from uuid import UUID
from typing import AsyncIterator
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.respositories.user_repository import UserRepository
from app.domain.entities.user_entity import User as DomainUser
from app.application.services.hasher_service import HasherService


class UserService:

    def __init__(
        self,
        user_repo: UserRepository,
        hasher_svc: HasherService,
        session_factory: AsyncIterator[AsyncSession],
    ):
        self.user_repo = user_repo
        self.hasher_svc = hasher_svc
        self.session_factory = session_factory

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
        async with self.session_factory() as session:
            return await self.user_repo.create(user=user, session=session)
    
    async def delete_user(self, id: UUID):
        async with self.session_factory() as session:
            await self.user_repo.delete(id=id, session=session)
