from chocs import HttpRequest, HttpResponse, HttpStatus, router
from gata import deserialise, validate
from kink import inject

from petstore.entities import Pet
from petstore.json_response import JsonResponse
from petstore.repositories import CategoryRepository, PetRepository


@router.post("/pets")
@inject()
def pets_create(
    request: HttpRequest,
    pet_repository: PetRepository,
    category_repository: CategoryRepository,
) -> HttpResponse:
    json_data = request.parsed_body.data
    try:
        validate(json_data, Pet)
    except ValueError as error:
        return HttpResponse(HttpStatus.PRECONDITION_FAILED, str(error))

    pet = deserialise(json_data, Pet)  # type: Pet

    category_repository.create(pet.category)
    pet_repository.create(pet)

    return JsonResponse(pet)


@router.get("/pets")
@inject()
def pets_list(request: HttpRequest, pet_repository: PetRepository) -> HttpResponse:
    return JsonResponse(pet_repository.find(request.query_string))


__all__ = ["pets_create", "pets_list"]
