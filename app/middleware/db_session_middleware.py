from starlette.types import ASGIApp, Receive, Scope, Send
from app.database.session import AsyncSessionLocal

class DBSessionMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        async with AsyncSessionLocal() as session:
            scope["state"] = {"db": session}
            await self.app(scope, receive, send)
