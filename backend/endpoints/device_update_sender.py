from starlette.endpoints import HTTPEndpoint
from starlette.types import Receive, Scope, Send
from starlette.responses import JSONResponse
from starlette.requests import Request


# TODO - possibly get rid of this file as we are sending 
# the module twin update from the svelte server side atm


class DeviceUpdateSenderEndpoint(HTTPEndpoint):
    def __init__(self, scope: Scope, receive: Receive, send: Send) -> None:
        super().__init__(scope, receive, send)
    
    async def get(self, request: Request):
        return JSONResponse({"message": "pong"}, status_code=200)
    
    async def post(self, request: Request):
        data = await request.json()
        colour = data["colour"]
        # TODO error handling
        return JSONResponse({"message": "pong"}, status_code=200)