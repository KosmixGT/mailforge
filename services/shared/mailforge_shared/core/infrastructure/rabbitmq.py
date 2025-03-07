import aio_pika
from mailforge_shared.core.interfaces.message_queue import MessageQueue
from typing import Any, Callable
import json
import asyncio

class RabbitMQQueue(MessageQueue):
    def __init__(self, connection_url: str):
        self.connection_url = connection_url
        self.connection = None
        self.channel = None
        
    async def connect(self) -> None:
        retries = 5
        while retries > 0:
            try:
                self.connection = await aio_pika.connect_robust(self.connection_url)
                self.channel = await self.connection.channel()
                await self.channel.declare_queue("mailings.created", durable=True)
                break
            except Exception:
                retries -= 1
                if retries == 0:
                    raise
                await asyncio.sleep(5)

    async def publish(self, routing_key: str, message: dict) -> None:
        if not self.channel:
            await self.connect()
        
        message_body = json.dumps(message).encode()
        await self.channel.default_exchange.publish(
            aio_pika.Message(body=message_body),
            routing_key=routing_key
        )

    async def subscribe(self, topic: str, callback: Callable) -> None:
        if not self.channel:
            await self.connect()

        queue = await self.channel.declare_queue(topic)
        
        async def process_message(message):
            async with message.process():
                await callback(json.loads(message.body.decode()))

        await queue.consume(process_message)
    
    async def close(self) -> None:
        if self.connection:
            await self.connection.close()
            self.connection = None
            self.channel = None
