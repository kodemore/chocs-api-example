from petstore.entities import Pet
from petstore.json_response import JsonResponse


def test_json_response():
    pet = Pet.create({
        "id": 1,
        "name": "Johny",
        "status": 1,
        "category": {
            "id": 2,
            "name": "Dogs",
        },
    })

    response = JsonResponse(pet)

    assert response.body == b'{"id": 1, "name": "Johny", "category": {"id": 2, "name": "Dogs"}, "status": 1}'

