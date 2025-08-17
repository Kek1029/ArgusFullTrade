import json
import logging
from typing import Callable, Dict, Any, Optional
from aio_pika import connect_robust, Message, ExchangeType
from aio_pika.abc import AbstractIncomingMessage
from pydantic import BaseModel


class BrokerMessage(BaseModel):
    type: str
    payload: Dict[str, Any]
    meta: Optional[Dict[str, str]] = None

class QueueBinding(BaseModel):
    exchange: str
    routing_key: str
    queue_name: str
    durable: bool = True
    auto_delete: bool = False


class RoutingRabbitClient:
    def __init__(self, url: str, routing_map: Dict[str, str]):
        self.url = url
        self.routing_map = routing_map
        self.reverse_map = {v: k for k, v in routing_map.items()}
        self.connection = None
        self.channel = None

    async def connect(self):
        self.connection = await connect_robust(self.url)
        self.channel = await self.connection.channel()

    async def publish(self, exchange_name: str, routing_key: str, msg: BrokerMessage):
        exchange = await self.channel.declare_exchange(exchange_name, ExchangeType.DIRECT, durable=True)
        body = msg.model_dump_json().encode("utf-8")
        await exchange.publish(
            Message(body, content_type="application/json"),
            routing_key=routing_key
        )

    async def _subscribe(self, binding: QueueBinding, handler: Callable[[BrokerMessage], Any]):
        exchange = await self.channel.declare_exchange(binding.exchange, ExchangeType.DIRECT, durable=True)
        queue = await self.channel.declare_queue(
            binding.queue_name,
            durable=binding.durable,
            auto_delete=binding.auto_delete
        )
        await queue.bind(exchange, routing_key=binding.routing_key)

        async def on_message(message: AbstractIncomingMessage):
            async with message.process():
                try:
                    data = BrokerMessage.model_validate_json(message.body.decode())
                    await handler(data)
                except Exception as e:
                    logging.error(f"Failed to process message: {e}")

        await queue.consume(on_message)

    async def close(self):
        await self.channel.close()
        await self.connection.close()
