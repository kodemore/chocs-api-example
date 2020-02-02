import datetime

from chocs import HttpRequest, HttpResponse, router

from chinook.json_response import JsonResponse
from .albums import *
from .artists import *


@router.get("/")
def ping(request: HttpRequest) -> HttpResponse:
    return JsonResponse({"pong": True, "server_time": datetime.datetime.now().isoformat()})
