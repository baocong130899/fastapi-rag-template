from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from loguru import logger
from app.bootstrap.container import Container
from app.presentation.api.v1.endpoints.base_router import api_router
from app.config.logger_config import configure_logging


@asynccontextmanager
async def lifespan(app: FastAPI):

    # Get container from state.
    container: Container = app.state._state.get("container")

    # Check connection.
    if not await container.session_manager().connect():
        raise RuntimeError("Cannot connect to database!.")
    logger.info("Connect to database successfully!.")

    logger.info("Initialize app successfully!.")

    yield

    # Close connection.
    await container.session_manager().close()
    logger.info("Close connect to database successfully!.")

    # Close logs.
    logger.info("Logs completed!.")
    await logger.complete()


def create_app(container: Container):

    # Get settings.
    settings = container.settings()

    # Init logger.
    configure_logging(settings=settings)

    # Declare app.
    app = FastAPI(
        lifespan=lifespan,
        title=settings.APP_NAME,
    )

    # Declare cors.
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    logger.info("Initialize cors successfully!.")

    # Declare routers.
    app.include_router(api_router, prefix="/api/v1")
    logger.info("Initialize routers successfully!.")

    # Add state.
    app.state.container = container
    logger.info("Initialize state successfully!.")

    return app


container = Container()
app = create_app(container=container)
