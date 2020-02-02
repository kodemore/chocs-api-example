from chocs import HttpStatus
from tests.utils import response_to_json


def test_create_artist(api_client) -> None:
    response = api_client.post("/artists", {"name": "Boo",})

    assert response.status_code == HttpStatus.OK
    body = response_to_json(response)

    assert "id" in body
