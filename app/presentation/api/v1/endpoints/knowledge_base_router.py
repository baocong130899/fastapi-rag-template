from typing import Annotated
from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide
from app.bootstrap.container import Container
from app.infrastructure.messaging import BaseMessagingClient

router = APIRouter()


@router.get("/")
@inject
async def knowledge(
    messaging_client: BaseMessagingClient = Depends(Provide[Container.messaging_client]),
):
    await messaging_client.publish(payload={
        "a": "b"
    })
