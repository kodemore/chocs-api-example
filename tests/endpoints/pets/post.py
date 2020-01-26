from chocs import HttpMethod, HttpStatus


def test_create_pet_200(api_client) -> None:
    response = api_client(HttpMethod.POST, "/pets", {
        "name": "Boo",
        "category": {
            "name": "Test",
        },
        "status": 1,
    })

    assert response.status_code == HttpStatus.OK
    body = api_client.get_json_body()

    assert "id" in body
    assert "id" in body["category"]


