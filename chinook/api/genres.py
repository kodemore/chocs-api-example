from chinook.json_response import JsonResponse
from chinook.repositories import GenreRepository
from chinook.utils import Paginator
from chocs import HttpRequest, HttpResponse, router
from gata import serialise
from kink import inject


@router.get("/genres")
@inject()
def genres_list(request: HttpRequest, repository: GenreRepository) -> HttpResponse:
    paginator = Paginator(request.query_string, "/genres", allow_fields=["name"])
    items = []
    for item in repository.find_by_paginator(paginator):
        items.append(serialise(item))

    return JsonResponse({"body": items, **paginator.hateos})


__all__ = ["genres_list"]
