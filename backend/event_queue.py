import asyncio
from typing import Optional

from loguru import logger
from backend.settings import settings
from backend.service_bus import receive
from azure.servicebus.exceptions import MessagingEntityNotFoundError


TOPIC="orin03-dev"
SUBSCRIPTION="subscription-1"
SENTINEL = object()


class EventQueue:
    def __init__(self) -> None:
        self.forward_task: Optional[asyncio.Task] = None
        self.subscribers: dict[str, asyncio.Queue]= {}
    
    async def start(self):
        self.forward_task = asyncio.create_task(self.reader())

    async def close(self):
        self.forward_task.cancel()
        await self.forward_task
        exc = self.forward_task.exception()
        if exc:
            logger.exception(exc)
            raise
    
    async def __aenter__(self):
        await self.start()
    
    async def __aexit__(self, exc_type, exc_value, exc_tb):
        await self.close()

    async def reader(self):
        logger.info(f"Backend is reading events from service bus topic {TOPIC}")

        try:
            async for message in receive(
                conn_str=settings.SERVICE_BUS_CONN_STRING,
                topic=TOPIC,
                subscription=SUBSCRIPTION,
            ):  
                for id_, queue in self.subscribers.items():
                    queue.put_nowait(message)
        except asyncio.CancelledError:
            pass
        except MessagingEntityNotFoundError as err:
            logger.exception("Could not read from service bus")
            raise
        except Exception as err:
            logger.exception(err)
            raise
        finally:
            logger.info(f"Backend stopped reading from service bus topic {TOPIC}")
    
    def subscribe(self) -> asyncio.Queue:
        queue = asyncio.Queue()
        sub_id = id(queue)
        logger.info(f"Creating subscription ID {sub_id}")
        self.subscribers[sub_id] = queue
        return queue
    
    def unsubscribe(self, queue: asyncio.Queue) -> None:
        sub_id = id(queue)
        logger.info(f"Removing subscription ID {sub_id}")
        queue = self.subscribers[sub_id]
        queue.put_nowait(SENTINEL)
        self.subscribers.pop(sub_id)
