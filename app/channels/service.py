from typing import List
from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.session import Session
from starlette import status
from app.db_models import Channel as DbChannel
from app.schemas import Channel as APIChannel


class ChannelException(HTTPException):
    pass

def get_channel_by_id(db_session: Session, channel_id: int) -> APIChannel:
    try:
        db_channel = db_session.query(DbChannel).filter(DbChannel.id == channel_id).first()
        return APIChannel(id=db_channel.id, name=db_channel.name)
    except AttributeError:
        raise ChannelException(status_code=status.HTTP_404_NOT_FOUND, detail="Channel not found")


def get_all_channels(db_session: Session) -> List[APIChannel]:
    db_channels = db_session.query(DbChannel).all()
    api_channels = list()
    for db_channel in db_channels:
        api_channels.append(APIChannel(id=db_channel.id, name=db_channel.name))
    return api_channels

def create_channel(db_session: Session, new_channel_name: str) -> APIChannel:
    try:
        db_channel = DbChannel(name=new_channel_name)
        db_session.add(db_channel)
        db_session.commit()
        db_session.refresh(db_channel)
        return APIChannel(id=db_channel.id, name=db_channel.name)
    except IntegrityError:
        raise ChannelException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Channel name already exists")


def update_channel_name(db_session: Session, channel_id: int, new_channel_name: str) -> APIChannel:
    try:
        db_channel = db_session.query(DbChannel).filter(DbChannel.id == channel_id).first()
        db_channel.name = new_channel_name
        db_session.commit()
        db_session.refresh(db_channel)
        return APIChannel(id=db_channel.id, name=db_channel.name)
    except AttributeError:
        raise ChannelException(status_code=status.HTTP_404_NOT_FOUND, detail="Channel not found")
    except IntegrityError:
        raise ChannelException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Channel name already exists")


def delete_channel_by_id(db_session: Session, channel_id: int):
    rows_deleted = db_session.query(DbChannel).filter(DbChannel.id == channel_id).delete()
    if rows_deleted == 0:
        raise ChannelException(status_code=status.HTTP_404_NOT_FOUND, detail="Channel not found")
    db_session.commit()
