from typing import Callable

from jimmy import JSONResponse, Request, Headers


class JimmyHandler:

    http_methods = {"get", "post", "put", "patch", "delete", "options", "head"}

    async def __call__(self, request: Request):
        handler = getattr(self, request.method.value.lower(), None)

        if handler is None:
            return JSONResponse(
                body={
                    "error": "Method Not Allowed",
                },
                status_code=405,
            )

        return await handler(request)

    async def get(self, request: Request): ...

    async def post(self, request: Request): ...

    async def put(self, request: Request): ...

    async def patch(self, request: Request): ...

    async def delete(self, request: Request): ...

    async def head(self, request: Request): ...

    async def options(self, request: Request): ...

    async def __allowed_methods(self):
        methods = [
            m.upper()
            for m in self.http_methods
            if getattr(self, m, None) is not None
        ]
        return ", ".join(methods)

    async def handle_head(self, request: Request):
        head_method = self.__class__.head

        if head_method is not JimmyHandler.head:
            return await self.head(request)

        get_method: Callable = getattr(self, "get", None)
        if get_method is None:
            headers = Headers.json_to_bytes(
                obj={"Allow": self.__allowed_methods()}
            )
            return JSONResponse(headers=headers, status_code=405)

        response = await get_method(request)

        response.body = b""
        return response



