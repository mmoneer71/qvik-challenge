from typing import List, Optional
from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.orm.session import Session

from app.samples import sample_article, sample_article_list, sample_422, sample_404, sample_bckgrnd
from app.schemas import Article, ArticleCreate, ArticleUpdate
from app.articles import service as ArticlesService
from app.database import get_db_session

articles_router = APIRouter()

@articles_router.get(
    "/",
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
    "/{article_id}",
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
    "/",
    responses={
        200: {
            "model": str,
            "description": "Article will be created in background",
            "content": {"application/json": {"example": sample_bckgrnd}},
        },
        404: {
            "description": "Channel not found",
            "content": {"application/json": {"example": sample_404}},
        },
        422: {
            "description": "Invalid input format",
            "content": {"application/json": {"example": sample_422}},
        },
    },
)
def add_article(new_article: ArticleCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db_session)) -> str:
    resp = ArticlesService.validate_article_and_channel(db_session=db, channel_id=new_article.channel_id, article_url=str(new_article.url))
    background_tasks.add_task(ArticlesService.create_article, db_session=db, channel_id=new_article.channel_id, article_url=str(new_article.url))
    return resp


@articles_router.put(
    "/",
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
def update_article_channel(updated_article: ArticleUpdate, db: Session = Depends(get_db_session)) -> Article:
    return ArticlesService.update_article(db_session=db, article_id=updated_article.id, new_channel_name=updated_article.channel_name)

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
