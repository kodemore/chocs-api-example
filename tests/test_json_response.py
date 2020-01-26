from petstore.entities import Pet
from petstore.json_response import JsonResponse
from gata import deserialise


def test_json_response():
    pet = deserialise({
        "id": 1,
        "name": "Johny",
        "status": 1,
        "category": {
            "id": 2,
            "name": "Dogs",
        },
    }, Pet)

    response = JsonResponse(pet)

    assert response.body.read() == b'{"id": 1, "name": "Johny", "category": {"id": 2, "name": "Dogs"}, "status": 1}'

