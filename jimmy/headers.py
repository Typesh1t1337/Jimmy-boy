import json


class Headers:
    def __init__(self, headers_byte: bytes | None):
        self.headers_byte = headers_byte

    def json(self):
        if self.headers_byte is None:
            raise TypeError('No headers_byte specified')
        parsed = {k.decode(): v.decode() for k, v in self.headers_byte}
        return parsed

    @classmethod
    def json_to_bytes(cls, obj: dict):
        byte_header = json.dumps(obj, separators=(',', ':'), sort_keys=True).encode()
        return cls(byte_header)
