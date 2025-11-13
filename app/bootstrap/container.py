from httpx import AsyncClient, Client, Limits
from dependency_injector import containers, providers
from app.config.settings import Settings
from app.infrastructure.database import SessionManager
from app.infrastructure.repository_impl.user_repository_impl import (
    SQLAlchemyUserRepository,
)
from app.infrastructure.repository_impl.token_impl import (
    SqlAlchemyTokenRepository,
)
from app.application.services.user_service import UserService
from app.application.services.auth_service import AuthService
from app.application.services.jwt_service import JwtService
from app.application.services.hasher_service import HasherService
from app.ai.adapters.chunking import RecursiveCharacterAdapter
from app.ai.adapters.document_loading import (
    TextAdapter,
    PyPDFAdapter,
)
from app.ai.factories import LoaderFactory
from app.ai.adapters.embedding import (
    AzureOpenAIEmbeddingsAdapter,
    JinaEmbeddingsAdapter,
)
from app.ai.adapters.vectorstore import (
    PostgresVectorStoreAdapter,
)
from app.ai.adapters.llm import (
    AzureOpenAILLMAdapter,
    OllamaLLMAdapter,
)
from app.ai.pipelines import (
    IndexingPipeline
)
from app.infrastructure.messaging import RabbitMQClient


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=[
            "app.presentation.api",
            "app.presentation.api.v1.endpoints",
        ]
    )

    settings = providers.Singleton(Settings)
    session_manager = providers.Singleton(SessionManager, settings=settings)
    user_repository = providers.Factory(SQLAlchemyUserRepository)
    token_repository = providers.Factory(SqlAlchemyTokenRepository)

    async_client = providers.Singleton(
        AsyncClient,
        timeout=settings.provided.HTTP_CLIENT_TIMEOUT, 
        limits=Limits(max_connections=100, max_keepalive_connections=20)
    )
    sync_client = providers.Singleton(
        Client,
        timeout=settings.provided.HTTP_CLIENT_TIMEOUT, 
        limits=Limits(max_connections=100, max_keepalive_connections=20)
    )

    hasher_service = providers.Singleton(HasherService)
    jwt_service = providers.Factory(
        JwtService,
        secret=settings.provided.JWT_SECRET,
        algorithm=settings.provided.JWT_ALGORITHM,
        access_expires=settings.provided.JWT_ACCESS_EXPIRES_IN,
        refresh_expires=settings.provided.JWT_REFRESH_EXPIRES_IN,
    )
    user_service = providers.Factory(
        UserService,
        user_repo=user_repository,
        hasher_svc=hasher_service,
        session_factory=session_manager.provided.async_generator,
    )
    auth_service = providers.Factory(
        AuthService,
        user_repo=user_repository,
        token_repo=token_repository,
        jwt_svc=jwt_service,
        hasher_svc=hasher_service,
        session_factory=session_manager.provided.async_generator,
    )

    loader_factory = providers.Singleton(
        LoaderFactory,
        factory_aggregate=providers.FactoryAggregate(
            txt=providers.Singleton(TextAdapter),
            pdf=providers.Singleton(PyPDFAdapter, mode=settings.provided.PAGE_MODE),
        ),
    )
    text_splitter = providers.Selector(
        selector=settings.provided.CHUNKING_ADAPTER,
        recursive_character=providers.Singleton(
            RecursiveCharacterAdapter,
            chunk_size=settings.provided.CHUNK_SZIE,
            chunk_overlap=settings.provided.CHUNK_OVERLAP,
            separators=settings.provided.SEPARATORS,
        ),
    )
    embeddings = providers.Selector(
        selector=settings.provided.EMBEDDINGS_ADAPTER.value,
        azure_openai_embeddings=providers.Singleton(
            AzureOpenAIEmbeddingsAdapter,
            model=settings.provided.AZURE_OPENAI_API_EMBEDDING_NAME,
            deployment=settings.provided.AZURE_OPENAI_API_EMBEDDING_DEPLOYMENT_NAME,
            api_version=settings.provided.AZURE_OPENAI_API_EMBEDDING_VERSION,
            endpoint=settings.provided.AZURE_OPENAI_API_EMBEDDING_ENDPOINT,
            api_key=settings.provided.AZURE_OPENAI_API_EMBEDDING_KEY,
            http_async_client=async_client,
            http_client=sync_client,
        ),
        jina_embeddings=providers.Singleton(
            JinaEmbeddingsAdapter,
            model=settings.provided.JINA_EMBEDDINGS_NAME, 
            api_key=settings.provided.JINA_EMBEDDINGS_KEY,
        ),
    )
    vector_store = providers.Singleton(
        PostgresVectorStoreAdapter,
        embeddings_function=embeddings.provided.get_embed,
        engine=session_manager.provided.get_engine.call(),
    )
    llm_chat = providers.Selector(
        selector=settings.provided.LLM_ADAPTER.value,
        azure_openai_llm=providers.Singleton(
            AzureOpenAILLMAdapter,
            model=settings.provided.AZURE_OPENAI_API_LLM_NAME,
            endpoint=settings.provided.AZURE_OPENAI_API_LLM_ENDPOINT,
            api_version=settings.provided.AZURE_OPENAI_API_LLM_VERSION,
            api_key=settings.provided.AZURE_OPENAI_API_LLM_KEY,
            temperature=settings.provided.TEMPERATURE,
            top_p=settings.provided.TOP_P,
            http_async_client=async_client,
            http_client=sync_client,
        ),
        ollama_llm=providers.Singleton(
            OllamaLLMAdapter,
            model=settings.provided.OLLAMA_API_LLM_NAME,
            endpoint=settings.provided.OLLAMA_API_LLM_ENDPOINT,
            temperature=settings.provided.TEMPERATURE,
            top_p=settings.provided.TOP_P,
        ),
    )
    indexing_pipeline = providers.Factory(
        IndexingPipeline,
        loader_factory=loader_factory,
        text_splitter=text_splitter,
        embedder=embeddings,
        vector_store=vector_store,
    )
    print(settings.provided.get_rabbitmq_url(), flush=True)
    messaging_client = providers.Singleton(
        RabbitMQClient,
        url=settings.provided.get_rabbitmq_url(),
        prefetch_count=settings.provided.RABBITMQ_PREFETCH_COUNT,
    )