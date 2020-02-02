from chocs import HttpStatus
from tests.utils import response_to_json


def test_get_artist(api_client) -> None:
    response = api_client.get("/artists")

    assert response.status_code == HttpStatus.OK
