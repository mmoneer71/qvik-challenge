from http import HTTPStatus
from fastapi.testclient import TestClient

from app.samples import sample_urls


def test_create_article(app_client: TestClient, clean_state):
    json_data = {"name": "DummyChannel"}
    app_client.post("/channels/", json=json_data)
    json_data = {"name": "DummyChannel2"}
    app_client.post("/channels/", json=json_data)
    json_data = {"url": sample_urls[0], "channel_id": "1"}
    response = app_client.post("/articles/", json=json_data)
    assert response.status_code == HTTPStatus.OK
    assert response.json() == "Article will be fetched and created in the background"
    article = app_client.get("/articles/1")
    assert article.json() == {
        "id": 1,
        "url": "https://edition.cnn.com/2020/09/21/us/arctic-sea-ice-shrunk-minimum-extent-2020-scn-trnd/index.html",
        "channel_id": 1,
        "word_count": 473,
    }


def test_get_articles(app_client: TestClient):
    json_data = {"url": sample_urls[1], "channel_id": 1}
    app_client.post("/articles/", json=json_data)
    response = app_client.get("/articles/")
    assert len(response.json()) == 2
    assert response.json() == [
        {
            "id": 1,
            "url": "https://edition.cnn.com/2020/09/21/us/arctic-sea-ice-shrunk-minimum-extent-2020-scn-trnd/index.html",
            "channel_id": 1,
            "word_count": 473,
        },
        {
            "id": 2,
            "url": "https://edition.cnn.com/2021/10/06/us/gabby-petito-brian-laundrie-update-wednesday/index.html",
            "channel_id": 1,
            "word_count": 139,
        },
    ]


def test_update_article_channel_name(app_client: TestClient):
    json_data = {"id": 1, "channel_name": "DummyChannel2"}
    response = app_client.put("/articles/", json=json_data)
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "id": 1,
        "url": "https://edition.cnn.com/2020/09/21/us/arctic-sea-ice-shrunk-minimum-extent-2020-scn-trnd/index.html",
        "channel_id": 2,
        "word_count": 473,
    }


def test_delete_article(app_client: TestClient):
    app_client.delete("/articles/2")
    response = app_client.get("/articles/2")
    assert response.status_code == HTTPStatus.NOT_FOUND
