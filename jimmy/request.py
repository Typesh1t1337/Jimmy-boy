import json
from wsgiref.headers import Headers

from jimmy import Method


class Request:
    def __init__(self,
                 method: Method,
                 url: str,
                 body: bytes,
                 headers: Headers
                 ):
        self.method = method
        self.url = url
        self.headers = headers
        self.body = body

    @classmethod
    async def from_asgi(cls, scope, receive):
        method = scope["method"]
        path = scope["path"]

        method_enum = Method(method)

        if scope["type"] == "http":
            headers_raw = scope["headers"]
            headers = Headers(headers_raw)
        else:
            headers = None

        body = b""
        while True:
            msg = await receive()
            if msg["type"] == "http.request":
                body += msg.get("body", b"")
                if not msg.get("more_body", False):
                    break

        return cls(method=method_enum, url=path, body=body, headers=headers)

    async def json(self):
        if not self.body:
            return None

        return json.loads(self.body.decode("utf-8"))