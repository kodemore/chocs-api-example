from chinook.json_response import JsonResponse
from chinook.repositories.albums_repository import AlbumsRepository
from chinook.utils import Paginator
from chocs import HttpRequest, HttpResponse, router
from gata import serialise
from kink import inject


@router.get("/albums")
@inject()
def albums_list(request: HttpRequest, repository: AlbumsRepository) -> HttpResponse:
    paginator = Paginator(
        request.query_string, "/albums", allow_fields=["title", "artist.name"]
    )
    items = []
    for item in repository.find_by_paginator(paginator):
        items.append(serialise(item))

    return JsonResponse({"body": items, **paginator.hateos})
