import json
import asyncio
from aio_pika import (
    Message, 
    DeliveryMode,
)
from aio_pika.abc import AbstractIncomingMessage, AbstractRobustExchange

async def process_message(
    message: AbstractIncomingMessage,
    dlx_ex: AbstractRobustExchange,

) -> None:
    data = json.loads(message.body.decode())
    print(data, flush=True)

    if message.redelivered:
        print("Message ak when rabbitmq connection error", flush=True)
        await message.ack()
    
    limit = 1
    if message.headers.get("x-retry-count") == limit:
        print("Message ack because x-retry-count > limit", flush=True)
        await message.ack()

    print("Start 20s!", flush=True)
    await asyncio.sleep(20)
    print("End 20s!", flush=True)

    await message.reject(requeue=True)
    print("Message Reject and send to delay", flush=True)