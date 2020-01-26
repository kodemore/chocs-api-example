import sqlite3
from io import BytesIO
from json import dumps, loads
from petstore.api import *
import pytest
from chocs import Headers, HttpMethod, HttpRequest, HttpResponse, router
from chocs.middleware import MiddlewarePipeline
from kink import di

from petstore.middleware import check_json_request

di[sqlite3.Connection] = lambda di: sqlite3.connect(di["database_path"])


def _create_json_request(method: HttpMethod, uri: str, body: dict) -> HttpRequest:
    json_body = dumps(body).encode("utf8")
    return HttpRequest(
        method,
        uri,
        BytesIO(json_body),
        headers=Headers({"Content-Type": "application/json"})
    )


class ApiClient:
    def __init__(self):
        self.middleware = MiddlewarePipeline()
        self.middleware.append(check_json_request, router)
        self.responses = []
        self.request: HttpRequest
        self.response: HttpResponse

    def __call__(self, method: HttpMethod, uri: str, body: dict) -> HttpResponse:
        request = _create_json_request(method, uri, body)
        self.request = request
        self.response = self.middleware(request)
        self.responses.append(self.response)

        return self.response

    def get_json_body(self) -> dict:
        return loads(self.response.body.read().decode("utf8"))


@pytest.fixture()
def api_client() -> ApiClient:
    return ApiClient()
