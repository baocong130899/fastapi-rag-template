from typing import Optional, List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr, Field, field_validator
from app.infrastructure.enums.environment_enum import EnvironmentType
from app.ai.enums import (
    ChunkingProvider, 
    PageModeProvider,
    EmbeddingsProvider,
    LLMProvider,
)


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

    RABBITMQ_USER: str = "guest"
    RABBITMQ_PASS: SecretStr = "guest"
    RABBITMQ_HOST: str = "localhost"
    RABBITMQ_PORT: int = 5672
    RABBITMQ_VHOST: str = "/"
    RABBITMQ_URI: Optional[str] = None
    RABBITMQ_PREFETCH_COUNT: int = 2

    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_EXPIRES_IN: int = 3600  # 1h.
    JWT_REFRESH_EXPIRES_IN: int = 86400 * 7  # 7 day.

    CHUNKING_ADAPTER: ChunkingProvider = ChunkingProvider.RECURSIVE_CHARACTER.value
    CHUNK_SZIE: int = 1024
    CHUNK_OVERLAP: int = 250
    SEPARATORS: List[str] = [
        "\n\n",
        "\n",
        " ",
        ".",
        ",",
        "\u200b",  # Zero-width space
        "\uff0c",  # Fullwidth comma
        "\u3001",  # Ideographic comma
        "\uff0e",  # Fullwidth full stop
        "\u3002",  # Ideographic full stop
        "",
    ]

    PAGE_MODE: PageModeProvider = PageModeProvider.PAGE.value

    HTTP_CLIENT_TIMEOUT: float = 30

    EMBEDDINGS_ADAPTER: EmbeddingsProvider = Field(..., description="Which embeddings adapter to use.")
    # Azure embeddings fields.
    AZURE_OPENAI_API_EMBEDDING_NAME: Optional[str] = None
    AZURE_OPENAI_API_EMBEDDING_DEPLOYMENT_NAME: Optional[str] = None
    AZURE_OPENAI_API_EMBEDDING_ENDPOINT: Optional[str] = None
    AZURE_OPENAI_API_EMBEDDING_VERSION: Optional[str] = None
    AZURE_OPENAI_API_EMBEDDING_KEY: Optional[str] = None
    # Jina ebeddings fields.
    JINA_EMBEDDINGS_NAME: Optional[str] = None
    JINA_EMBEDDINGS_KEY: Optional[str] = None

    LLM_ADAPTER: LLMProvider = Field(..., description="Which llm adapter to use.")
    TEMPERATURE: float = 0.3
    TOP_P: float = 0.9
    # Azure llm fields.
    AZURE_OPENAI_API_LLM_NAME: Optional[str] = None
    AZURE_OPENAI_API_LLM_ENDPOINT: Optional[str] = None
    AZURE_OPENAI_API_LLM_VERSION: Optional[str] = None
    AZURE_OPENAI_API_LLM_KEY: Optional[str] = None
    # Ollama llm fields.
    OLLAMA_API_LLM_NAME: Optional[str] = None
    OLLAMA_API_LLM_ENDPOINT: Optional[str] = None

    @field_validator(
        "AZURE_OPENAI_API_EMBEDDING_NAME", 
        "AZURE_OPENAI_API_EMBEDDING_DEPLOYMENT_NAME",
        "AZURE_OPENAI_API_EMBEDDING_ENDPOINT",
        "AZURE_OPENAI_API_EMBEDDING_VERSION",
        "AZURE_OPENAI_API_EMBEDDING_KEY",
        mode="after"
    )
    @classmethod
    def _check_azure_fields(cls, v, info):
        if info.data.get("EMBEDDINGS_ADAPTER") == EmbeddingsProvider.AZURE_OPENAI_EMBEDDINGS:
            if v is None or (isinstance(v, str) and v.strip() == ""):
                raise ValueError(f"{info.field_name} is required when EMBEDDINGS_ADAPTER is {EmbeddingsProvider.AZURE_OPENAI_EMBEDDINGS.value!r}")
        return v

    @field_validator("JINA_EMBEDDINGS_NAME", "JINA_EMBEDDINGS_KEY", mode="after")
    @classmethod
    def _check_jina_fields(cls, v, info):
        if info.data.get("EMBEDDINGS_ADAPTER") == EmbeddingsProvider.JINA_EMBEDDINGS:
            if v is None or (isinstance(v, str) and v.strip() == ""):
                raise ValueError(f"{info.field_name} is required when EMBEDDINGS_ADAPTER is {EmbeddingsProvider.JINA_EMBEDDINGS.value!r}")
        return v
    
    @field_validator(
        "AZURE_OPENAI_API_LLM_NAME", 
        "AZURE_OPENAI_API_LLM_ENDPOINT", 
        "AZURE_OPENAI_API_LLM_VERSION",
        "AZURE_OPENAI_API_LLM_KEY",
        mode="after"
    )
    @classmethod
    def _check_azure_llm_fields(cls, v, info):
        if info.data.get("LLM_ADAPTER") == LLMProvider.AZURE_OPENAI_LLM:
            if v is None or (isinstance(v, str) and v.strip() == ""):
                raise ValueError(f"{info.field_name} is required when LLM_ADAPTER is {LLMProvider.AZURE_OPENAI_LLM.value!r}")
        return v
    
    @field_validator("OLLAMA_API_LLM_NAME", "OLLAMA_API_LLM_ENDPOINT", mode="after")
    @classmethod
    def _check_ollama_fields(cls, v, info):
        if info.data.get("LLM_ADAPTER") == LLMProvider.OLLAMA_LLM:
            if v is None or (isinstance(v, str) and v.strip() == ""):
                raise ValueError(f"{info.field_name} is required when LLM_ADAPTER is {LLMProvider.OLLAMA_LLM.value!r}")
        return v

    @property
    def get_database_url(self) -> str:
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD.get_secret_value()}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )
    
    @property
    def get_rabbitmq_url(self) -> str:
        if self.RABBITMQ_URI:
            return self.RABBITMQ_URI
        return (
            f"amqp://{self.RABBITMQ_USER}:{self.RABBITMQ_PASS.get_secret_value()}@{self.RABBITMQ_HOST}:{self.RABBITMQ_PORT}/{self.RABBITMQ_VHOST}"
        )
