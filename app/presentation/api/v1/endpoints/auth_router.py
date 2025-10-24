from typing import Annotated
from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide
from app.bootstrap.container import Container
from app.presentation.api.dependencies import get_current_user
from app.presentation.schemas.auth_schemas import AuthLogin, AuthResponse, AuthRefreshResponse
from app.application.services.auth_service import AuthService
from app.presentation.schemas.user_schemas import UserResponse
from app.presentation.api.dependencies import oauth2_scheme


router = APIRouter()


@router.post("/login")
@inject
async def login(
    form_data: Annotated[AuthLogin, Depends(AuthLogin.as_form)],
    auth_svc: AuthService = Depends(Provide[Container.auth_service]),
):
    result = await auth_svc.login(email=form_data.username, password=form_data.password)
    return AuthResponse(
        access_token=result.access_token, refresh_token=result.refresh_token
    )


@router.post("/refresh")
@inject
async def refresh(
    refresh_token: str = Depends(oauth2_scheme),
    auth_svc: AuthService = Depends(Provide[Container.auth_service]),
):
    result = await auth_svc.refresh(refresh_token=refresh_token)
    return AuthRefreshResponse(access_token=result.access_token)


@router.get("/me")
async def me(current_user: UserResponse = Depends(get_current_user)):
    return current_user


@router.post("/logout", status_code=200)
@inject
async def logout(
    current_user: UserResponse = Depends(get_current_user),
    auth_svc: AuthService = Depends(Provide[Container.auth_service]),
):
    await auth_svc.revoke_token(user_id=current_user.id)
