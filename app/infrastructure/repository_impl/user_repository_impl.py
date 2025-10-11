from typing import AsyncIterator, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.domain.respositories.user_repository import UserRepository
from app.domain.entities.user_entity import User as DomainUser
from app.infrastructure.models.user_model import UserModel


class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session_factory: AsyncIterator[AsyncSession]):
        self.session_factory = session_factory

    async def create(self, user: DomainUser) -> DomainUser:
        """"""
        async with self.session_factory() as session:
            session: AsyncSession

            model = UserModel(
                email=user.email,
                name=user.name,
                is_active=user.is_active,
                hashed_password=user.hashed_password,
            )
            session.add(model)
            await session.commit()
            await session.refresh(model)

            return DomainUser(
                id=str(model.id),
                email=user.email,
                name=model.name,
                is_active=model.is_active,
                hashed_password=model.hashed_password,
                created_at=model.created_at,
                updated_at=model.updated_at,
            )

    async def get_by_email(self, email: str) -> Optional[DomainUser]:
        """"""
        async with self.session_factory() as session:
            session: AsyncSession

            result = await session.execute(
                select(UserModel).where(UserModel.email == email)
            )
            model = result.scalar_one_or_none()
            if model:
                return DomainUser(
                    id=str(model.id),
                    email=model.email,
                    name=model.name,
                    is_active=model.is_active,
                    hashed_password=model.hashed_password,
                    created_at=model.created_at,
                    updated_at=model.updated_at,
                )

    async def get_by_id(self, id: str) -> Optional[DomainUser]:
        """"""
        async with self.session_factory() as session:
            session: AsyncSession

            result = await session.execute(select(UserModel).where(UserModel.id == id))
            model = result.scalar_one_or_none()
            if model:
                return DomainUser(
                    id=str(model.id),
                    email=model.email,
                    name=model.name,
                    is_active=model.is_active,
                    hashed_password=model.hashed_password,
                    created_at=model.created_at,
                    updated_at=model.updated_at,
                )

    async def list_all(self) -> List[DomainUser]:
        """"""

    async def delete(self, id: str) -> bool:
        """"""

    async def update(self, user: DomainUser) -> DomainUser:
        """"""
