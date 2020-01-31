from chinook.entities import Artist
from chinook.json_response import JsonResponse
from gata import deserialise


def test_json_response():

    response = JsonResponse({"id": 1, "name": "Poro",})

    assert response.body.read() == b'{"id": 1, "name": "Poro"}'
