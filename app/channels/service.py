from typing import List
from sqlalchemy.orm.session import Session
from app.db_models import Channel as DbChannel
from app.schemas import Channel


def get_channel(db_session: Session, channel_id: int) -> Channel:
    return db_session.query(Channel).filter(Channel.id == channel_id).first()


def get_channels(db_session: Session) -> List[Channel]:
    return db_session.query(Channel).all()


def create_channel(db_session: Session, new_channel_name: str) -> Channel:
    db_channel = DbChannel(name=new_channel_name)
    db_session.add(db_channel)
    db_session.commit()
    db_session.refresh(db_channel)
    return Channel(**db_channel.dict())


def update_channel(db_session: Session, channel_id: int, new_channel_name: str) -> Channel:
    db_channel = db_session.query(Channel).filter(Channel.id == channel_id).first()
    db_channel.name = new_channel_name
    db_session.commit()
    db_session.refresh(db_channel)
    return Channel(**db_channel.dict())


def delete_channel(db_session: Session, channel_id: int):
    db_session.query(Channel).filter(Channel.id == channel_id).delete()
