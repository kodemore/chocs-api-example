from chocs import HttpRequest, HttpResponse, HttpStatus, HttpMethod
from chocs.message import JsonBody
from chocs.middleware import MiddlewareHandler


def check_json_request(request: HttpRequest, next: MiddlewareHandler) -> HttpResponse:
    if request.method in (
        HttpMethod.POST,
        HttpMethod.PUT,
        HttpMethod.PATCH,
    ) and not isinstance(request.parsed_body, JsonBody):
        return HttpResponse(
            HttpStatus.BAD_REQUEST, "Request must be valid json request."
        )

    return next(request)


__all__ = ["check_json_request"]
