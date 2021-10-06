from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm.session import Session

from app.channels.service import get_channel_by_id, get_all_channels
from app.samples import sample_404, sample_422, sample_channel, sample_channel_list
from app.schemas import Channel
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
async def get_channels(db: Session = Depends(get_db_session)) -> List[Channel]:
    return get_all_channels(db_session=db)


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
async def get_channel(channel_id: int, db: Session = Depends(get_db_session)) -> List[Channel]:
    try:
        return get_channel_by_id(db_session=db, channel_id=channel_id)
    except AttributeError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Channel not found")
