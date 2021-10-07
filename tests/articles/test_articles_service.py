import pytest
from http import HTTPStatus

from app.articles import service as ArticlesService
from app.channels import service as ChannelsService
from app.samples import sample_urls
from app.schemas import Article
from tests.conftest import test_session, close_session


def test_create_article(clean_state):
    db_session = test_session()
    new_channel = ChannelsService.create_channel(
        db_session=db_session, new_channel_name="DummyChannel"
    )
    new_article = ArticlesService.create_article(
        db_session=db_session, article_url=sample_urls[0], channel_id=new_channel.id
    )
    assert new_article.id == 1
    assert new_article.url == sample_urls[0]
    assert new_article.word_count == 473
    assert (
        ArticlesService.get_article_by_id(db_session=db_session, article_id=1)
        == new_article
    )
    close_session(db_session)


def test_create_invalid_article():
    with pytest.raises(ArticlesService.ArticleException) as exc:
        db_session = test_session()
        ArticlesService.create_article(
            db_session=db_session, article_url="random.com.url", channel_id=1
        )
        close_session(db_session)
    assert exc.value.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert exc.value.detail == "Invalid article URL"
    close_session(db_session)


def test_get_invalid_article():
    with pytest.raises(ArticlesService.ArticleException) as exc:
        db_session = test_session()
        assert ArticlesService.get_article_by_id(db_session=db_session, article_id=12)
    assert exc.value.status_code == HTTPStatus.NOT_FOUND
    assert exc.value.detail == "Article not found"
    close_session(db_session)


def test_get_all_articles():
    db_session = test_session()
    new_channel = ChannelsService.create_channel(
        db_session=db_session, new_channel_name="DummyChannel2"
    )
    ArticlesService.create_article(
        db_session=db_session, article_url=sample_urls[1], channel_id=new_channel.id
    )
    assert ArticlesService.get_articles(db_session=db_session) == [
        Article(id=1, url=sample_urls[0], channel_id=1, word_count=473),
        Article(id=2, url=sample_urls[1], channel_id=2, word_count=139),
    ]
    close_session(db_session)


def test_get_articles_with_min_max():
    db_session = test_session()
    articles = ArticlesService.get_articles(
        db_session=db_session, min_words=100, max_words=200
    )
    assert len(articles) == 1
    assert articles[0].id == 2
    close_session(db_session)


def test_update_article_channel_name():
    db_session = test_session()
    ArticlesService.update_article(
        db_session=db_session, article_id=1, new_channel_name="DummyChannel2"
    )
    assert (
        ArticlesService.get_article_by_id(
            db_session=db_session, article_id=1
        ).channel_id
        == 2
    )
    close_session(db_session)


def test_update_article_invalid_channel():
    with pytest.raises(ArticlesService.ArticleException) as exc:
        db_session = test_session()
        ArticlesService.update_article(
            db_session=db_session, article_id=1, new_channel_name="CoolChannel"
        )
    assert exc.value.status_code == HTTPStatus.NOT_FOUND
    assert exc.value.detail == "Channel name or article not found"
    close_session(db_session)


def test_update_invalid_article():
    with pytest.raises(ArticlesService.ArticleException) as exc:
        db_session = test_session()
        ArticlesService.update_article(
            db_session=db_session, article_id=15, new_channel_name="DummyChannel2"
        )
    assert exc.value.status_code == HTTPStatus.NOT_FOUND
    assert exc.value.detail == "Channel name or article not found"
    close_session(db_session)


def test_delete_article():
    db_session = test_session()
    ArticlesService.delete_article_by_id(db_session=db_session, article_id=1)
    with pytest.raises(ArticlesService.ArticleException) as exc:
        ArticlesService.get_article_by_id(db_session=db_session, article_id=1)
    assert exc.value.status_code == HTTPStatus.NOT_FOUND
    assert exc.value.detail == "Article not found"
    close_session(db_session)


def test_delete_invalid_article():
    with pytest.raises(ArticlesService.ArticleException) as exc:
        db_session = test_session()
        ArticlesService.delete_article_by_id(db_session=db_session, article_id=15)
    assert exc.value.status_code == HTTPStatus.NOT_FOUND
    assert exc.value.detail == "Article not found"
    close_session(db_session)


def test_validate_invalid_url():
    with pytest.raises(ArticlesService.ArticleException) as exc:
        db_session = test_session()
        ArticlesService.validate_article_and_channel(
            db_session=db_session, article_url="page.com", channel_id=1
        )
    assert exc.value.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert exc.value.detail == "Article must be a .html page"
    close_session(db_session)


def test_validate_invalid_channel():
    with pytest.raises(ArticlesService.ArticleException) as exc:
        db_session = test_session()
        ArticlesService.validate_article_and_channel(
            db_session=db_session, article_url="article.html", channel_id=15
        )
    assert exc.value.status_code == HTTPStatus.NOT_FOUND
    assert exc.value.detail == "Channel not found"
    close_session(db_session)


def test_validate_article_already_exists():
    with pytest.raises(ArticlesService.ArticleException) as exc:
        db_session = test_session()
        ArticlesService.validate_article_and_channel(
            db_session=db_session, article_url=sample_urls[1], channel_id=1
        )
    assert exc.value.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert exc.value.detail == "Article URL already exists"
    close_session(db_session)
