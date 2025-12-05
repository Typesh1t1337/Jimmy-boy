from typing import Callable

from jimmy.__internal.__asgi_wrapper import ASGIWrapper


class Jimmy:
    def __init__(self):
        self.__handlers: dict = dict()

    def add_router(self, router: dict):
        self.__handlers = {
            **self.__handlers,
            **router
        }

    def add_handler(self, handler: ASGIWrapper, path: str):
        self.__handlers[path] = {
            "handler": handler,
            "path": path
        }

    def get_app(self):
        routes = self.__handlers

        async def app(scope, receive, send):
            path = scope["path"]
            handler_dict = routes.get(path)
            method = scope["method"]
            if not handler_dict:
                await send({
                    "type": "http.response.start",
                    "status": 404,
                    "headers": []
                })
                await send({
                    "type": "http.response.body",
                    "body": b"Not found",
                })
                return
            handler = handler_dict["handler"]
            handler_path = handler_dict["path"]
            handler_method: Callable = getattr(handler, method)
            if handler_method is None:
                await send({
                    "type": "http.response.start",
                    "status": 405,
                    "headers": [(b"content-type", b"text/plain")],
                })
                await send({
                    "type": "http.response.body",
                    "body": b"Method not allowed",
                })
                return

            args = []
            handler_parts = handler_path.strip("/").split("/")
            request_parts = path.strip("/").split("/")

            for h, r in zip(handler_parts, request_parts):
                if h.startswith("{") and h.endswith("}"):
                    args.append(r)

        return app



