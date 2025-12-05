import json
from typing import Any

from jimmy import Headers


class JSONResponse:
    def __init__(self,
                 body: dict[Any, Any] | None = None,
                 headers: Headers | None = None,
                 status_code: int = 200,
                 ):
        self.status_code = status_code
        self.body = body
        self.headers = headers

    def __to_json(self):
        if not self.body:
            return None
        return json.dumps(self.body)