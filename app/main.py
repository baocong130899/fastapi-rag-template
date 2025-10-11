from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.bootstrap.container import Container
from app.presentation.api.v1.endpoints.base_router import api_router


def init_container() -> Container:
    container = Container()
    return container


def configure_cors(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@asynccontextmanager
async def lifespan(app: FastAPI):

    # Init container.
    container = init_container()
    app.state.container = container

    # Get settings.
    settings = container.settings()

    # Set app.
    app.title = settings.APP_NAME
    app.openapi_version

    # Check connection.
    if not await container.session_manager().connect():
        raise RuntimeError("❌ Cannot connect to database!.")

    print("✅ Database connection OK!.", flush=True)

    yield

    # Close connection.
    await container.session_manager().close()


def create_app():
    # Declare app.
    app = FastAPI(lifespan=lifespan)

    # Declare cors.
    configure_cors(app)

    # Declare routers.
    app.include_router(api_router, prefix="/api/v1")

    return app


app = create_app()
