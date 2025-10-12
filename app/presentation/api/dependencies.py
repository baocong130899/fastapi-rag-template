from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from dependency_injector.wiring import inject, Provide
from app.bootstrap.container import Container
from app.application.services.auth_service import AuthService
from app.domain.entities.user_entity import User as DomainUser
from app.presentation.schemas.user_schemas import UserResponse


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login", refreshUrl="api/v1/auth/refresh"
)


@inject
async def get_current_user(
    access_token: str = Depends(oauth2_scheme),
    auth_svc: AuthService = Depends(Provide[Container.auth_service]),
) -> DomainUser:
    """"""
    try:
        user = await auth_svc.verify_access(access_token=access_token)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or revoked token!.",
        )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found!."
        )

    return UserResponse(
        id=str(user.id),
        name=user.name,
        email=user.email,
        is_active=user.is_active,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )
