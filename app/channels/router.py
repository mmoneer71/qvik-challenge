from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session

from app.channels import service as ChannelsService
from app.samples import (
    sample_404,
    sample_422,
    sample_article_list,
    sample_channel,
    sample_channel_list,
)
from app.schemas import Article, Channel, ChannelCreate
from app.database import get_db_session


channels_router = APIRouter()


@channels_router.get(
    "/",
    responses={
        200: {
            "model": List[Channel],
            "description": "Channels retreived successfully",
            "content": {"application/json": {"example": sample_channel_list}},
        }
    },
)
def get_channels(db: Session = Depends(get_db_session)) -> List[Channel]:
    return ChannelsService.get_all_channels(db_session=db)


@channels_router.get(
    "/{channel_id}",
    responses={
        200: {
            "model": Channel,
            "description": "Channel retreived successfully",
            "content": {"application/json": {"example": sample_channel}},
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
def get_channel(channel_id: int, db: Session = Depends(get_db_session)) -> Channel:
    return ChannelsService.get_channel_by_id(db_session=db, channel_id=channel_id)


@channels_router.get(
    "/{channel_id}/articles",
    responses={
        200: {
            "model": List[Article],
            "description": "Channel Articles retreived successfully",
            "content": {"application/json": {"example": sample_article_list}},
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
def get_channel_articles(
    channel_id: int, db: Session = Depends(get_db_session)
) -> List[Article]:
    return ChannelsService.get_channel_articles(db_session=db, channel_id=channel_id)


@channels_router.post(
    "/",
    responses={
        200: {
            "model": Channel,
            "description": "Channel created successfully",
            "content": {"application/json": {"example": sample_channel}},
        },
        422: {
            "description": "Invalid input format",
            "content": {"application/json": {"example": sample_422}},
        },
    },
)
def add_channel(
    new_channel: ChannelCreate, db: Session = Depends(get_db_session)
) -> Channel:
    return ChannelsService.create_channel(
        db_session=db, new_channel_name=new_channel.name
    )


@channels_router.put(
    "/",
    responses={
        200: {
            "model": Channel,
            "description": "Channel updated successfully",
            "content": {"application/json": {"example": sample_channel}},
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
def update_channel(
    updated_channel: Channel, db: Session = Depends(get_db_session)
) -> Channel:
    return ChannelsService.update_channel_name(
        db_session=db,
        channel_id=updated_channel.id,
        new_channel_name=updated_channel.name,
    )


@channels_router.delete(
    "/{channel_id}",
    responses={
        200: {
            "description": "Channel deleted successfully",
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
def delete_channel(channel_id: int, db: Session = Depends(get_db_session)) -> str:
    ChannelsService.delete_channel_by_id(db_session=db, channel_id=channel_id)
    return "Channel deleted successfully"
