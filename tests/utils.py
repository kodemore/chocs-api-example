from json import dumps, loads

from chocs import Headers, HttpMethod, HttpRequest, HttpResponse, router
from chocs.middleware import MiddlewarePipeline

from chinook.middleware import check_json_request
from chinook.api import *


def response_to_json(response: HttpResponse) -> dict:
    return loads(response.body.read().decode("utf8"))


def create_json_request(method: HttpMethod, uri: str, body: dict = None) -> HttpRequest:

    request = HttpRequest(
        method, uri, headers=Headers({"Content-Type": "application/json"})
    )

    if body:
        json_body = dumps(body).encode("utf8")
        request.body.write(json_body)

    return request


class ApiClient:
    def __init__(self):

        self.middleware = MiddlewarePipeline()
        self.middleware.append(check_json_request, router)
        self.responses = []
        self.request: HttpRequest = None  # type: ignore
        self.response: HttpResponse = None  # type: ignore

    def make_request(self, request: HttpRequest) -> HttpResponse:
        self.request = request
        self.response = self.middleware(request)
        self.responses.append(self.response)

        return self.response

    def post(self, uri: str, body: dict) -> HttpResponse:
        request = create_json_request(HttpMethod.POST, uri, body)
        return self.make_request(request)

    def get(self, uri: str) -> HttpResponse:
        request = create_json_request(HttpMethod.GET, uri)

        return self.make_request(request)


__all__ = ["response_to_json", "create_json_request", "ApiClient"]
