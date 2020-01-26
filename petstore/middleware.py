from chocs import HttpRequest, HttpResponse, HttpStatus
from chocs.message import JsonBody
from chocs.middleware import MiddlewareHandler


def check_json_request(request: HttpRequest, next: MiddlewareHandler) -> HttpResponse:
    if not isinstance(request.parsed_body, JsonBody):
        return HttpResponse(HttpStatus.BAD_REQUEST, "Request must be valid json request.")

    return next(request)


__all__ = ["check_json_request"]
