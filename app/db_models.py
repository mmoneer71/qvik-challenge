from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class Channel(Base):
    __tablename__ = "channels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)

    articles = relationship("Article", back_populates="parent_channel")


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, index=True, unique=True)
    word_count = Column(Integer, index=True)
    channel_id = Column(Integer, ForeignKey("channels.id"))

    parent_channel = relationship("Channel", back_populates="articles")
