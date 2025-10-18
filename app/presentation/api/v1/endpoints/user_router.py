from uuid import UUID
from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide
from app.bootstrap.container import Container
from app.application.services.user_service import UserService
from app.presentation.schemas.user_schemas import UserCreate, UserResponse


router = APIRouter()


@router.get("")
# @inject
async def all():
    pass


@router.get("/{id}")
# @inject
async def get_by_id(
    id: UUID, service: UserService = Depends(Provide[Container.user_service])
):
    pass


@router.post("/")
@inject
async def create(
    payload: UserCreate, service: UserService = Depends(Provide[Container.user_service])
):
    user = await service.create_user(
        email=payload.email,
        name=payload.name,
        is_active=payload.is_active,
        password=payload.password,
    )

    return UserResponse(
        id=str(user.id),
        name=user.name,
        email=user.email,
        is_active=user.is_active,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


@router.put("/{id}")
# @inject
async def update(
    id: UUID, 
    payload: str,
    service: UserService = Depends(Provide[Container.user_service])
):
    pass


@router.delete("/{id}")
# @inject
async def delete(
    id: UUID, service: UserService = Depends(Provide[Container.user_service])
):
    pass
