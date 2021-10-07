from http import HTTPStatus
from fastapi.testclient import TestClient


def test_index(app_client: TestClient):
    response = app_client.get("/")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Nothing to see here :eyes:"}
