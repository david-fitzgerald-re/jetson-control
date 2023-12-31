import asyncio
from typing import Any, Coroutine
from starlette.types import Receive, Scope, Send
from starlette.websockets import WebSocket
from loguru import logger
from starlette.endpoints import WebSocketEndpoint

from backend.event_queue import SENTINEL
from backend import events


class DeviceUpdateReceiverEndpoint(WebSocketEndpoint):
    """
    TODO
    """
    def __init__(self, scope: Scope, receive: Receive, send: Send) -> None:
        self.forward_task = None
        super().__init__(scope, receive, send)

    async def on_connect(self, websocket: WebSocket) -> Coroutine[Any, Any, None]:
        logger.info("Client connecting")

        self.forward_task = asyncio.create_task(self.forward(websocket))

        await websocket.accept()

        logger.info("Client connected")
    
    async def on_disconnect(self, websocket: WebSocket, close_code: int) -> Coroutine[Any, Any, None]:
        logger.info("Client disconnecting")

        self.forward_task.cancel()
        await self.forward_task

        logger.info("Client disconnected")

    async def forward(self, websocket: WebSocket):
        queue = events.subscribe()

        try:
            while True:
                message = await queue.get()
                await websocket.send_json(message)
                if message is SENTINEL:
                    logger.info("Received SENTINEL - exiting subscription")
                    break
        except asyncio.CancelledError:
            logger.info("Stopping forwarding messages to client")
        except Exception:
            raise
        finally:
            events.unsubscribe(queue)