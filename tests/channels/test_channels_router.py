from http import HTTPStatus
from fastapi.testclient import TestClient

from app.samples import sample_urls

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

def test_get_channel_articles(app_client: TestClient):
    json_data = {"url": sample_urls[0], "channel_id": 1}
    app_client.post("/articles/", json=json_data)
    json_data = {"url": sample_urls[1], "channel_id": 1}
    app_client.post("/articles/", json=json_data)
    response = app_client.get("/channels/1/articles/")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == [{"id": 1, "url": "https://edition.cnn.com/2020/09/21/us/arctic-sea-ice-shrunk-minimum-extent-2020-scn-trnd/index.html", "channel_id": 1, "word_count": 473},
                                {"id": 2, "url": "https://edition.cnn.com/2021/10/06/us/gabby-petito-brian-laundrie-update-wednesday/index.html", "channel_id": 1, "word_count": 139}]
