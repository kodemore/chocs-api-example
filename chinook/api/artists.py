from chocs import HttpRequest, HttpResponse, HttpStatus, router
from gata import deserialise, validate, serialise
from kink import inject

from chinook.entities import Artist
from chinook.json_response import JsonResponse
from chinook.repositories import ArtistRepository
from chinook.utils import Paginator


@router.post("/artists")
@inject()
def artists_create(
    request: HttpRequest, artist_repository: ArtistRepository,
) -> HttpResponse:
    json_data = request.parsed_body.data
    try:
        validate(json_data, Artist)
    except ValueError as error:
        return HttpResponse(HttpStatus.PRECONDITION_FAILED, str(error))

    entity = deserialise(json_data, Artist)  # type: Artist
    artist_repository.create(entity)

    return JsonResponse(serialise(entity))


@router.get("/artists")
@inject()
def artists_list(
    request: HttpRequest, artist_repository: ArtistRepository
) -> HttpResponse:
    paginator = Paginator(request.query_string, "/artists", allow_fields=["name"])
    items = []
    for item in artist_repository.find_by_paginator(paginator):
        items.append(serialise(item))

    return JsonResponse({"body": items, **paginator.hateos})


@router.get("/artists/{id}")
@inject()
def artists_get(
    request: HttpRequest, artist_repository: ArtistRepository
) -> HttpResponse:
    try:
        artist = artist_repository.get(request.attributes.get("id"))
    except IndexError:
        return JsonResponse(
            {"error": "Record not found", "body": None}, HttpStatus.NOT_FOUND
        )

    return JsonResponse({"body": serialise(artist)})


@router.delete("/artists/{id}")
@inject()
def artists_delete(
    request: HttpRequest, artist_repository: ArtistRepository
) -> HttpResponse:
    try:
        artist = artist_repository.get(request.attributes.get("id"))
    except IndexError:
        return JsonResponse(
            {"error": "Record not found", "body": None}, HttpStatus.NOT_FOUND
        )

    artist_repository.delete(artist)

    return JsonResponse({"body": serialise(artist)})


__all__ = ["artists_create", "artists_list", "artists_get", "artists_delete"]
