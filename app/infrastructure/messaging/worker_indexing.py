import json
from typing import Dict, Any
from aio_pika import (
    Message, 
    DeliveryMode,
)
from aio_pika.abc import AbstractIncomingMessage, AbstractRobustExchange


async def on_message(
    message: AbstractIncomingMessage,
    retry_ex: AbstractRobustExchange,
    max_retries: int,

) -> None:
    headers = dict(message.headers or {})
    retries = int(headers.get("x-retry-count", 0))

    try:
        # Channel or connection reset or RabbitMQ connection error..
        if message.redelivered:
            await message.ack()
            
        data = json.loads(message.body.decode())
        print(message, flush=True)
        print(data, flush=True)
        await message.ack()
    except Exception as e:
        print(e, flush=True)
        await message.ack()
    

    # retry_msg = Message(body=message.body, headers=headers)
    # await retry_ex.publish(retry_msg, routing_key=routing_key)
    # await message.ack()
    # logger.info("Republished message %s to retry tier %d (routing %s)", message.message_id or "<no-id>", next_retry, routing_key)


async def process_payload(data: Dict[str, Any]):
    pass