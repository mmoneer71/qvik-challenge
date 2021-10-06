from typing import List
from sqlalchemy.orm.session import Session
from app.db_models import Channel as DbChannel
from app.schemas import Channel as APIChannel


def get_channel_by_id(db_session: Session, channel_id: int) -> APIChannel:
    db_channel = db_session.query(DbChannel).filter(DbChannel.id == channel_id).first()
    return APIChannel(id=db_channel.id, name=db_channel.name)


def get_all_channels(db_session: Session) -> List[APIChannel]:
    db_channels = db_session.query(DbChannel).all()
    api_channels = list()
    for db_channel in db_channels:
        api_channels.append(APIChannel(id=db_channel.id, name=db_channel.name))
    return api_channels

def create_channel(db_session: Session, new_channel_name: str) -> APIChannel:
    db_channel = DbChannel(name=new_channel_name)
    db_session.add(db_channel)
    db_session.commit()
    db_session.refresh(db_channel)
    return APIChannel(id=db_channel.id, name=db_channel.name)


def update_channel(db_session: Session, channel_id: int, new_channel_name: str) -> APIChannel:
    db_channel = db_session.query(DbChannel).filter(DbChannel.id == channel_id).first()
    db_channel.name = new_channel_name
    db_session.commit()
    db_session.refresh(db_channel)
    return APIChannel(id=db_channel.id, name=db_channel.name)


def delete_channel(db_session: Session, channel_id: int):
    db_session.query(DbChannel).filter(DbChannel.id == channel_id).delete()
