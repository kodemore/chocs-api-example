from io import BytesIO
from json import dumps
from typing import Any

from chocs import HttpResponse, HttpStatus


class JsonResponse(HttpResponse):
    def __init__(self, body: Any, status: HttpStatus = HttpStatus.OK):
        super().__init__(status)
        self.headers.set("content-type", "application/json")
        self._body = body

    @property
    def body(self) -> BytesIO:
        return BytesIO(dumps(self._body).encode("utf-8"))

    @body.setter
    def body(self, value) -> None:
        pass
