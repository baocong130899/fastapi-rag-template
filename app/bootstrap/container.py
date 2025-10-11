from dependency_injector import containers, providers
from app.config.settings import Settings
from app.infrastructure.database import SessionManager
from app.infrastructure.repository_impl.user_repository_impl import (
    SQLAlchemyUserRepository,
)
from app.application.services.user_service import UserService
from app.application.services.auth_service import AuthService
from app.application.services.jwt_service import JwtService
from app.application.services.hasher_service import HasherService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=[
            "app.presentation.api",
            "app.presentation.api.v1.endpoints",
        ]
    )
    settings = providers.Singleton(Settings)
    session_manager = providers.Singleton(SessionManager, settings=settings)
    user_repository = providers.Factory(
        SQLAlchemyUserRepository,
        session_factory=session_manager.provided.async_generator,
    )
    hasher_service = providers.Singleton(HasherService)
    user_service = providers.Factory(
        UserService,
        user_repo=user_repository,
        hasher_svc=hasher_service,
    )
    jwt_service = providers.Factory(
        JwtService,
        secret=settings.provided.JWT_SECRET,
        algorithm=settings.provided.JWT_ALGORITHM,
        access_expires=settings.provided.JWT_ACCESS_EXPIRES_IN,
        refresh_expires=settings.provided.JWT_REFRESH_EXPIRES_IN,
    )
    auth_service = providers.Factory(
        AuthService,
        user_repo=user_repository,
        jwt_svc=jwt_service,
        hasher_svc=hasher_service,
    )
