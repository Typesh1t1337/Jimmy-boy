import enum


class Method(enum.Enum):
    get = enum.auto()
    post = enum.auto()
    put = enum.auto()
    delete = enum.auto()
    head = enum.auto()
