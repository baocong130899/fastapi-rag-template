from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr
from app.infrastructure.enums.environment_enum import EnvironmentType


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    APP_NAME: str
    ENVIRONMENT: EnvironmentType = EnvironmentType.DEVELOPMENT.value  #
    VERSION: str = "0.1.0"

    LOG_LEVEL: str = "INFO"
    LOG_JSON_FORMAT: bool = False
    LOG_MESSAGE_FILE: str = "logs/app.log"
    LOG_ERROR_FILE: str = "logs/error.log"
    LOG_BACKTRACE: bool = True
    LOG_DIAGNOSE: bool = False

    DATABASE_DEBUG: bool = False
    DATABASE_URL: Optional[str] = None
    POSTGRES_USER: str ="postgres"
    POSTGRES_PASSWORD: SecretStr ="postgres"
    POSTGRES_HOST: str = "127.0.0.1"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str = "pgvector"
    POOL_SIZE: int = 10
    MAX_OVERFLOW: int = 5
    POOL_RECYCLE: int = 1800

    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_EXPIRES_IN: int = 3600  # 1h.
    JWT_REFRESH_EXPIRES_IN: int = 86400 * 7  # 7 day.

    @property
    def get_database_url(self) -> str:
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD.get_secret_value()}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )
