from typing import List, Optional
from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm.session import Session
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from newspaper import ArticleException as ThirdPartyArticleException
from app.const import HTM_SUFFIX, HTML_SUFFIX
from app.db_models import Channel as DbChannel, Article as DbArticle
from app.schemas import Article as APIArticle
from app.articles.utils import fetch_article_url


class ArticleException(HTTPException):
    pass


def get_article_by_id(db_session: Session, article_id: int) -> APIArticle:
    try:
        db_article = (
            db_session.query(DbArticle).filter(DbArticle.id == article_id).first()
        )
        return APIArticle(
            id=db_article.id,
            url=db_article.url,
            channel_id=db_article.channel_id,
            word_count=db_article.word_count,
        )
    except AttributeError:
        raise ArticleException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Article not found"
        )


def get_articles(
    db_session: Session,
    min_words: Optional[int] = None,
    max_words: Optional[int] = None,
) -> List[APIArticle]:
    query = db_session.query(DbArticle)
    if min_words:
        query = query.filter(DbArticle.word_count >= min_words)
    if max_words:
        query = query.filter(DbArticle.word_count <= max_words)
    db_articles = query.all()
    api_articles = list()
    for db_article in db_articles:
        api_articles.append(
            APIArticle(
                id=db_article.id,
                url=db_article.url,
                channel_id=db_article.channel_id,
                word_count=db_article.word_count,
            )
        )
    return api_articles


def create_article(
    db_session: Session, article_url: str, channel_id: int
) -> APIArticle:
    try:
        article_word_count = fetch_article_url(article_url=article_url)
        db_article = DbArticle(
            url=article_url, channel_id=channel_id, word_count=article_word_count
        )
        db_session.add(db_article)
        db_session.commit()
        db_session.refresh(db_article)
        return APIArticle(
            id=db_article.id,
            url=db_article.url,
            channel_id=db_article.channel_id,
            word_count=db_article.word_count,
        )
    except ThirdPartyArticleException:
        raise ArticleException(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid article URL"
        )


def update_article(
    db_session: Session, article_id: int, new_channel_name: str
) -> APIArticle:
    try:
        channel_id = (
            db_session.query(DbChannel)
            .filter(DbChannel.name == new_channel_name)
            .first()
            .id
        )
        db_article = (
            db_session.query(DbArticle).filter(DbArticle.id == article_id).first()
        )
        db_article.channel_id = channel_id
        db_session.commit()
        db_session.refresh(db_article)
        return APIArticle(
            id=db_article.id,
            url=db_article.url,
            channel_id=db_article.channel_id,
            word_count=db_article.word_count,
        )
    except AttributeError:
        raise ArticleException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Channel name or article not found",
        )


def delete_article_by_id(db_session: Session, article_id: int):
    rows_deleted = (
        db_session.query(DbArticle).filter(DbArticle.id == article_id).delete()
    )
    if rows_deleted == 0:
        raise ArticleException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Article not found"
        )
    db_session.commit()


def validate_article_and_channel(
    db_session: Session, article_url: str, channel_id: int
) -> str:
    if not article_url.lower().endswith(
        HTML_SUFFIX
    ) and not article_url.lower().endswith(HTM_SUFFIX):
        raise ArticleException(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Article must be a .html page",
        )

    channel = db_session.query(DbChannel).filter(DbChannel.id == channel_id).first()
    article = db_session.query(DbArticle).filter(DbArticle.url.is_(article_url)).first()
    if not channel:
        raise ArticleException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Channel not found"
        )
    if article:
        raise ArticleException(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Article URL already exists",
        )
    return "Article will be fetched and created in the background"
