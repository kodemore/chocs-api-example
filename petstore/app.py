from chocs import HttpRequest
from chocs import HttpResponse
from chocs import HttpStatus
from chocs import router
from chocs import serve
from kink import di
from kink import inject
from json import dumps as dump_json

from petstore.db import create_database
from petstore.entities import Pet
from petstore.repositories.pet_repository import PetRepository

create_database(di['database_path'], di['database_schema'])


@router.post('/pets')
@inject()
def create_pet(request: HttpRequest, pet_repository: PetRepository) -> HttpResponse:
    pet = Pet.create(request.parsed_body.data)
    pet_repository.create(pet)
    return HttpResponse(HttpStatus.OK, dump_json(pet.serialise()))


serve(host="localhost", port=8080)
