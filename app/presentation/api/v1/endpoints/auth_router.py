from typing import Annotated
from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide
from app.bootstrap.container import Container
from app.presentation.api.dependencies import get_current_user
from app.presentation.schemas.auth_schemas import AuthLogin, AuthResponse
from app.application.services.auth_service import AuthService
from app.presentation.schemas.user_schemas import UserResponse


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
async def refresh():
    pass


@router.get("/me")
async def me(current_user: UserResponse = Depends(get_current_user)):
    return current_user

@router.post("/logout")
async def logout():
    pass
