from http import HTTPStatus
from fastapi.testclient import TestClient

def test_create_channel(app_client: TestClient, clean_state):
    json_data = {"name": "DummyChannel"}
    response = app_client.post("/channels/", json=json_data)
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"id": 1, "name": "DummyChannel"}

def test_get_all_channels(app_client: TestClient):
    json_data = {"name": "DummyChannel2"}
    response = app_client.post("/channels/", json=json_data)
    response = app_client.get("/channels/")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == [{"id": 1, "name": "DummyChannel"}, {"id": 2, "name": "DummyChannel2"}]

def test_get_channel_id(app_client: TestClient):
    response = app_client.get("/channels/1")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"id": 1, "name": "DummyChannel"}

def test_update_channel(app_client: TestClient):
    json_data = {"id": 1, "name": "NotDummyAfterAll"}
    response = app_client.put("/channels/", json=json_data)
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"id": 1, "name": "NotDummyAfterAll"}

def test_delete_channel(app_client: TestClient):
    app_client.delete("/channels/2")
    response = app_client.get("/channels/2")
    assert response.status_code == HTTPStatus.NOT_FOUND
