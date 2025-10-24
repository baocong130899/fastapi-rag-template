from uuid import UUID
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.domain.respositories.user_repository import UserRepository
from app.domain.entities.user_entity import User as DomainUser
from app.infrastructure.models.user_model import UserModel


class SQLAlchemyUserRepository(UserRepository):
    """Class representing a person"""

    async def create(self, user: DomainUser, session: AsyncSession) -> DomainUser:
        """"""
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

    async def get_by_email(self, email: str, session: AsyncSession) -> Optional[DomainUser]:
        """"""
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

    async def get_by_id(self, id: UUID, session: AsyncSession) -> Optional[DomainUser]:
        """"""
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

    async def list_all(self, session: AsyncSession) -> List[DomainUser]:
        """"""

    async def delete(self, id: UUID, session: AsyncSession) -> None:
        """"""
        await session.execute(delete(UserModel).where(UserModel.id == id))
        await session.commit()

    async def update(self, user: DomainUser, session: AsyncSession) -> DomainUser:
        """"""
