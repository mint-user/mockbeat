from enum import auto, Enum


class HTTPMethod(str, Enum):
    CONNECT = auto()
    DELETE = auto()
    GET = auto()
    HEAD = auto()
    OPTIONS = auto()
    PATCH = auto()
    POST = auto()
    PUT = auto()
    TRACE = auto()

    @classmethod
    def choices(cls):
        return [(item.value, item.name) for item in cls]
