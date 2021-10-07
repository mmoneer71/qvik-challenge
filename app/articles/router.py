from typing import List, Optional
from fastapi import APIRouter
from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session

from app.samples import sample_article, sample_article_list, sample_422, sample_404
from app.schemas import Article
from app.articles import service as ArticlesService
from app.database import get_db_session

articles_router = APIRouter()

@articles_router.get(
    "/articles",
    responses={
        200: {
            "model": List[Article],
            "description": "Articles retreived successfully",
            "content": {"application/json": {"example": sample_article_list}},
        }
    },
)
def get_articles(min_words: Optional[int] = None, max_words: Optional[int] = None,  db: Session = Depends(get_db_session)) -> List[Article]:
    return ArticlesService.get_articles(db_session=db, min_words=min_words, max_words=max_words)


@articles_router.get(
    "/articles/{article_id}",
    responses={
        200: {
            "model": Article,
            "description": "Article retreived successfully",
            "content": {"application/json": {"example": sample_article}},
        },
        404: {
            "description": "Article not found",
            "content": {"application/json": {"example": sample_404}},
        },
        422: {
            "description": "Article input format",
            "content": {"application/json": {"example": sample_422}},
        },
    },
)
def get_article(article_id: int, db: Session = Depends(get_db_session)) -> Article:
    return ArticlesService.get_article_by_id(db_session=db, article_id=article_id)

@articles_router.post(
    "/channels/{channel_name}/articles",
    responses={
        200: {
            "model": Article,
            "description": "Article created successfully",
            "content": {"application/json": {"example": sample_article}},
        },
        422: {
            "description": "Invalid input format",
            "content": {"application/json": {"example": sample_422}},
        },
    },
)
def add_article_by_channel_name(channel_name: str, article_url: str, db: Session = Depends(get_db_session)) -> Article:
    return ArticlesService.create_article_by_channel_name(db_session=db, channel_name=channel_name, article_url=article_url)


@articles_router.post(
    "/channels/{channel_id}/articles",
    responses={
        200: {
            "model": Article,
            "description": "Article created successfully",
            "content": {"application/json": {"example": sample_article}},
        },
        422: {
            "description": "Invalid input format",
            "content": {"application/json": {"example": sample_422}},
        },
    },
)
def add_article_by_channel_id(channel_id: int, article_url: str, db: Session = Depends(get_db_session)) -> Article:
    return ArticlesService.create_article_by_channel_id(db_session=db, channel_id=channel_id, article_url=article_url)


@articles_router.put(
    "/articles/{article_id}",
    responses={
        200: {
            "model": Article,
            "description": "Article updated successfully",
            "content": {"application/json": {"example": sample_article}},
        },
        404: {
            "description": "Article not found",
            "content": {"application/json": {"example": sample_404}},
        },
        422: {
            "description": "Invalid input format",
            "content": {"application/json": {"example": sample_422}},
        },
    },
)
def update_article_channel(article_id: int, channel_name: str, db: Session = Depends(get_db_session)) -> Article:
    return ArticlesService.update_article(db_session=db, article_id=article_id, new_channel_name=channel_name)

@articles_router.delete(
    "/{article_id}",
    responses={
        200: {
            "description": "Article deleted successfully",
        },
        404: {
            "description": "Article not found",
            "content": {"application/json": {"example": sample_404}},
        },
        422: {
            "description": "Invalid input format",
            "content": {"application/json": {"example": sample_422}},
        },
    },
)
def delete_article(article_id: int, db: Session = Depends(get_db_session)) -> str:
    ArticlesService.delete_article_by_id(db_session=db, article_id=article_id)
    return "Article deleted successfully"
