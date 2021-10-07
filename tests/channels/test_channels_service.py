import pytest
from http import HTTPStatus

from app.articles import service as ArticlesService
from app.channels import service as ChannelsService
from app.samples import sample_urls
from app.schemas import Article, Channel
from tests.conftest import test_session, close_session


def test_create_channel(clean_state):
    db_session = test_session()
    new_channel = ChannelsService.create_channel(
        db_session=db_session, new_channel_name="DummyChannel"
    )
    assert new_channel.id == 1
    assert new_channel.name == "DummyChannel"
    assert (
        ChannelsService.get_channel_by_id(db_session=db_session, channel_id=1)
        == new_channel
    )
    close_session(db_session)


def test_create_channel_already_exists():
    with pytest.raises(ChannelsService.ChannelException) as exc:
        db_session = test_session()
        ChannelsService.create_channel(
            db_session=db_session, new_channel_name="DummyChannel"
        )
    assert exc.value.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert exc.value.detail == "Channel name already exists"
    close_session(db_session)


def test_get_all_channels():
    db_session = test_session()
    ChannelsService.create_channel(
        db_session=db_session, new_channel_name="DummyChannel2"
    )
    assert ChannelsService.get_all_channels(db_session=db_session) == [
        Channel(id=1, name="DummyChannel"),
        Channel(id=2, name="DummyChannel2"),
    ]
    close_session(db_session)


def test_get_invalid_channel():
    with pytest.raises(ChannelsService.ChannelException) as exc:
        db_session = test_session()
        ChannelsService.get_channel_by_id(db_session=db_session, channel_id="12")
    assert exc.value.status_code == HTTPStatus.NOT_FOUND
    assert exc.value.detail == "Channel not found"
    close_session(db_session)


def test_update_channel():
    db_session = test_session()
    ChannelsService.update_channel_name(
        db_session=db_session, channel_id=1, new_channel_name="NotDummyAfterAll"
    )
    assert (
        ChannelsService.get_channel_by_id(db_session=db_session, channel_id=1).name
        == "NotDummyAfterAll"
    )
    close_session(db_session)


def test_update_channel_name_conflict():
    with pytest.raises(ChannelsService.ChannelException) as exc:
        db_session = test_session()
        ChannelsService.update_channel_name(
            db_session=db_session, channel_id=1, new_channel_name="DummyChannel2"
        )
    assert exc.value.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert exc.value.detail == "Channel name already exists"
    close_session(db_session)


def test_update_channel_invalid_id():
    with pytest.raises(ChannelsService.ChannelException) as exc:
        db_session = test_session()
        ChannelsService.update_channel_name(
            db_session=db_session, channel_id=12, new_channel_name="DummyChannel2"
        )
    assert exc.value.status_code == HTTPStatus.NOT_FOUND
    assert exc.value.detail == "Channel not found"
    close_session(db_session)


def test_delete_channel():
    db_session = test_session()
    ChannelsService.delete_channel_by_id(db_session=db_session, channel_id=2)
    with pytest.raises(ChannelsService.ChannelException) as exc:
        ChannelsService.get_channel_by_id(db_session=db_session, channel_id=2)
    assert exc.value.status_code == HTTPStatus.NOT_FOUND
    assert exc.value.detail == "Channel not found"
    close_session(db_session)


def test_delete_channel_invalid_id():
    with pytest.raises(ChannelsService.ChannelException) as exc:
        db_session = test_session()
        ChannelsService.delete_channel_by_id(db_session=db_session, channel_id=2)
    assert exc.value.status_code == HTTPStatus.NOT_FOUND
    assert exc.value.detail == "Channel not found"
    close_session(db_session)


def test_get_channel_articles():
    db_session = test_session()
    ArticlesService.create_article(
        db_session=db_session, article_url=sample_urls[0], channel_id=1
    )
    ArticlesService.create_article(
        db_session=db_session, article_url=sample_urls[1], channel_id=1
    )
    articles = ChannelsService.get_channel_articles(db_session=db_session, channel_id=1)
    assert len(articles) == 2
    assert articles == [
        Article(id=1, url=sample_urls[0], channel_id=1, word_count=473),
        Article(id=2, url=sample_urls[1], channel_id=1, word_count=139),
    ]
    close_session(db_session)


def test_get_invalid_channel_articles():
    with pytest.raises(ChannelsService.ChannelException) as exc:
        db_session = test_session()
        ChannelsService.get_channel_articles(db_session=db_session, channel_id=12)
    assert exc.value.status_code == HTTPStatus.NOT_FOUND
    assert exc.value.detail == "Channel not found"
    close_session(db_session)
