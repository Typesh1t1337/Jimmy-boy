from jimmy import Request
from jimmy.handler import JimmyHandler


class ASGIWrapper:
    def __init__(self, handler_cls: type[JimmyHandler]):
        self.handler = handler_cls()

    async def __call__(self, scope, receive, send):
        request = await Request.from_asgi(scope=scope, receive=receive)

        response = await self.handler(request)
        await send({
            "type": "http.response.start",
            "status": response.status,
            "headers": [(b"content-type", b"text/plain")]
        })
        await send({
            "type": "http.response.body",
            "body": response.body,
        })


