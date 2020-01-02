from json import dumps as dump_json

from chocs import HttpRequest
from chocs import HttpResponse
from chocs import HttpStatus
from chocs import router
from chocs import serve
from kink import di
from kink import inject

from petstore import create_database
from petstore.entities import Pet
from petstore.repositories import CategoryRepository
from petstore.repositories import PetRepository
from petstore.json_response import JsonResponse

create_database(di["database_path"], di["database_schema"])


@router.post("/pets")
@inject()
def create_pet(
    request: HttpRequest,
    pet_repository: PetRepository,
    category_repository: CategoryRepository,
) -> HttpResponse:
    pet = Pet.create(request.parsed_body.data)

    category_repository.create(pet.category)
    pet_repository.create(pet)

    return JsonResponse(pet)


@router.get("/pets")
@inject()
def list_pets(request: HttpRequest, pet_repository: PetRepository) -> HttpResponse:
    return JsonResponse(pet_repository.find(request.query_string))


serve(host="localhost", port=8080)
