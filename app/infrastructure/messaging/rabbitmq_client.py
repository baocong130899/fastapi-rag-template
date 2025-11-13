import json
from typing import Optional, Dict, Any
from aio_pika import (
    connect_robust, 
    ExchangeType, 
    Exchange,
    Message,
    DeliveryMode,
)
from aio_pika.abc import AbstractRobustConnection, AbstractRobustChannel
from .base_messaging_client import BaseMessagingClient
from .worker_indexing import process_message


class RabbitMQClient(BaseMessagingClient):
    
    def __init__(
        self, 
        url: str,
        prefetch_count: int,
        main_queue_name: str = "main_queue",
        main_exchange_name: str = "main_exchange",
        delay_queue_name: str = "delay_queue",
        dlx_exchange_name: str = "dlx_exchange",
        delay_ttl_ms: int = 15000
    ):
        self.url = url
        self.prefetch_count = prefetch_count
        self.main_queue_name = main_queue_name
        self.main_exchange_name = main_exchange_name
        self.delay_queue_name = delay_queue_name
        self.dlx_exchange_name = dlx_exchange_name
        self.delay_ttl_ms = delay_ttl_ms

        self.connection: Optional[AbstractRobustConnection] = None
        self.channel: Optional[AbstractRobustChannel] = None
        self.main_ex: Optional[Exchange] = None
    
    async def init(self):
        """"""

        # Robust connection will automatically try to reconnect.
        self.connection = await connect_robust(url=self.url, timeout=60, heartbeat=60, reconnect_interval=10)

        # Creating channel.
        self.channel = await self.connection.channel()

        # Maximum message count which will be processing at the same time.
        await self.channel.set_qos(prefetch_count=self.prefetch_count)

        # Declare exchanges.
        self.main_ex = await self.channel.declare_exchange(name=self.main_exchange_name, type=ExchangeType.DIRECT, durable=True)
        dlx_ex = await self.channel.declare_exchange(name=self.dlx_exchange_name, type=ExchangeType.DIRECT, durable=True)

        # Declaring delay queue: the message will stay here for a while and then go back to the main queue.
        delay_queue = await self.channel.declare_queue(
            name=self.delay_queue_name,
            durable=True,
            arguments={
                "x-dead-letter-exchange": self.main_exchange_name,
                "x-dead-letter-routing-key": self.main_queue_name,
                "x-message-ttl": self.delay_ttl_ms,
            },
        )
        await delay_queue.bind(exchange=dlx_ex, routing_key=self.delay_queue_name)

        # Declaring queue.
        main_queue = await self.channel.declare_queue(
            name=self.main_queue_name,
            durable=True,
            arguments={
                "x-dead-letter-exchange": self.dlx_exchange_name,
                "x-dead-letter-routing-key": self.delay_queue_name,
            },
        )
        await main_queue.bind(self.main_ex, routing_key=self.main_queue_name)

        # Consume queue.
        await main_queue.consume(lambda msg: process_message(message=msg, dlx_ex=dlx_ex))

    async def close(self):
        """"""
        await self.connection.close()
    
    async def publish(self, payload: Dict[str, Any]) -> None:
        """"""
        headers = {"x-retry-count": 0}
        message = Message(
            body=json.dumps(payload).encode(),
            headers=headers,
            content_type="application/json",
            delivery_mode=DeliveryMode.PERSISTENT,
        )
        await self.main_ex.publish(message=message, routing_key=self.main_queue_name)