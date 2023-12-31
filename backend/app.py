# TODO avoid annoying path manipulation
import sys
from pathlib import Path
parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir))

from starlette.applications import Starlette
from starlette.routing import WebSocketRoute
import uvicorn
from backend import events
from backend.endpoint import DeviceUpdateEndpoint


async def lifespan(app: Starlette):
    """
    Controls set-up and teardown actions for the app.
    """
    async with events:
        # Yield control to the app
        yield
        # App teardown


routes=[
    WebSocketRoute("/ws", endpoint=DeviceUpdateEndpoint)
]


app = Starlette(
    routes=routes,
    lifespan=lifespan,
)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)