from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from loguru import logger
from app.bootstrap.container import Container
from app.presentation.api.v1.endpoints.base_router import api_router
from app.config.logger_config import configure_logging


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
    logger.info("Creating the container successfully!.")

    # Get settings.
    settings = container.settings()

    # Set app.
    app.title = settings.APP_NAME
    app.openapi_version

    logger.info("Set the values to create the app successfully!.")

    # Check connection.
    if not await container.session_manager().connect():
        raise RuntimeError("Cannot connect to database!.")

    logger.info("Connect to database successfully!.")

    yield

    # Close connection.
    await container.session_manager().close()
    logger.info("Close connect to database successfully!.")

    await logger.complete()


def create_app():

    # Init logger.
    configure_logging()

    # Declare app.
    app = FastAPI(lifespan=lifespan)

    # Declare cors.
    configure_cors(app)
    logger.info("Initialize cors successfully!.")

    # Declare routers.
    app.include_router(api_router, prefix="/api/v1")
    logger.info("Initialize routers successfully!.")

    return app


app = create_app()
