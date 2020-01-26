from io import BytesIO
from json import JSONEncoder, dumps
from typing import Any

from chocs import HttpResponse, HttpStatus
from gata import serialise


def _to_json(self, obj):
    return serialise(obj)


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
