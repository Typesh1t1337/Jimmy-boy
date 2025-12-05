from jimmy.handler import JimmyHandler
from __internal.__asgi_wrapper import ASGIWrapper


class Router:
    def __init__(self):
        self.routes = {}
        self.prefix: str = ""

    def add_handler(self, handler: type[JimmyHandler], path: str):
        total_path = self.prefix + path
        self.routes[total_path] = {
            "path": total_path,
            "handler": ASGIWrapper(handler)
        }
