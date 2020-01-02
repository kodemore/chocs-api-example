from json import JSONEncoder
from json import dumps
from typing import Any

from chocs import HttpResponse
from chocs import HttpStatus
from io import BytesIO


def _to_json(self, obj):
    return getattr(obj.__class__, "serialise", _to_json.default)(obj)


_to_json.default = JSONEncoder.default  # Save unmodified default.
JSONEncoder.default = _to_json


class JsonResponse(HttpResponse):
    def __init__(self, o: Any, status: HttpStatus = HttpStatus.OK):
        super().__init__(status)
        self.headers.set("content-type", "application/json")
        self._body = o

    @property
    def body(self) -> BytesIO:
        return BytesIO(dumps(self._body).encode("utf-8"))

    @body.setter
    def body(self, value) -> None:
        pass
