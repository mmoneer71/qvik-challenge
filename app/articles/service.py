from typing import List, Optional
from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.session import Session
from newspaper import Article as NewspaperArticle, ArticleException as ThirdPartyArticleException

from app.db_models import Channel as DbChannel, Article as DbArticle
from app.schemas import Article as APIArticle
from app.articles.utils import strip_tags


class ArticleException(HTTPException):
    pass

def _fetch_article_url(article_url: str) -> int:
    try:
        news_article = NewspaperArticle(article_url, keep_article_html=True)
        news_article.download()
        news_article.parse()
        striped_article = strip_tags(news_article.article_html)
        return len(striped_article.strip().split(" "))
    except ThirdPartyArticleException:
        raise ArticleException(status_code=422, detail="Invalid article URL")

def get_article_by_id(db_session: Session, article_id: int) -> APIArticle:
    try:
        db_article = db_session.query(DbArticle).filter(DbArticle.id == article_id).first()
        return APIArticle(id=db_article.id, url=db_article.url, channel_id=db_article.channel_id, word_count=db_article.word_count)
    except AttributeError:
        raise ArticleException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")

def get_articles(db_session: Session, min_words: Optional[int], max_words: Optional[int]) -> List[APIArticle]:
    query = db_session.query(DbArticle)
    if min_words:
        query = query.filter(DbArticle.word_count >= min_words)
    if max_words:
        query = query.filter(DbArticle.word_count <= max_words)
    db_articles = query.all()
    api_articles = list()
    for db_article in db_articles:
        api_articles.append(APIArticle(id=db_article.id, url=db_article.url, channel_id=db_article.channel_id, word_count=db_article.word_count))
    return api_articles

def get_channel_articles(db_session: Session, channel_id: int) -> List[APIArticle]:
    db_articles = db_session.query(DbChannel).filter(DbChannel.id == channel_id).first().articles
    api_articles = list()
    for db_article in db_articles:
        api_articles.append(APIArticle(id=db_article.id, url=db_article.url, channel_id=db_article.channel_id, word_count=db_article.word_count))
    return api_articles

def create_article_by_channel_id(db_session: Session, channel_id: int, article_url: str) -> APIArticle:
    try:
        article_word_count = _fetch_article_url(article_url=article_url)
        db_article = DbArticle(url=article_url, channel_id=channel_id, word_count=article_word_count)
        db_session.add(db_article)
        db_session.commit()
        db_session.refresh(db_article)
        return APIArticle(id=db_article.id, url=db_article.url, channel_id=db_article.channel_id, word_count=db_article.word_count)
    except IntegrityError as err:
        raise ArticleException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Article URL already exists or Invalid channel ID")

def create_article_by_channel_name(db_session: Session, channel_name: str, article_url: str) -> APIArticle:
    try:
        article_word_count = _fetch_article_url(article_url=article_url)
        channel_id = db_session.query(DbChannel).filter(DbChannel.name == channel_name).first().id
        db_article = DbArticle(url=article_url, channel_id=channel_id, word_count=article_word_count)
        db_session.add(db_article)
        db_session.commit()
        db_session.refresh(db_article)
        return APIArticle(id=db_article.id, url=db_article.url, channel_id=db_article.channel_id, word_count=db_article.word_count)
    except IntegrityError:
        raise ArticleException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Article URL already exists")
    except AttributeError:
        raise ArticleException(status_code=status.HTTP_404_NOT_FOUND, detail="Channel not found")

def update_article(db_session: Session, article_id :int, new_channel_name: str) -> APIArticle:
    try:
        channel_id = db_session.query(DbChannel).filter(DbChannel.name == new_channel_name).first().id
        db_article = db_session.query(DbArticle).filter(DbArticle.id == article_id).first()
        db_article.channel_id = channel_id
        db_session.commit()
        db_session.refresh(db_article)
        return APIArticle(id=db_article.id, url=db_article.url, channel_id=db_article.channel_id, word_count=db_article.word_count)
    except AttributeError:
        raise ArticleException(status_code=status.HTTP_404_NOT_FOUND, detail="Channel name or article not found")

def delete_article_by_id(db_session: Session, article_id: int):
    rows_deleted = db_session.query(DbArticle).filter(DbArticle.id == article_id).delete()
    if rows_deleted == 0:
        raise ArticleException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
    db_session.commit()

