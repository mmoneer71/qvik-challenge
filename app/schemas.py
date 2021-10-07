from pydantic import BaseModel
from pydantic.networks import HttpUrl


class Message(BaseModel):
    message: str


class ChannelCreate(BaseModel):
    name: str

class Channel(ChannelCreate):
    id: int

    class Config:
        orm_mode = True

class ArticleCreate(BaseModel):
    url: HttpUrl
    channel_id: int

class ArticleUpdate(BaseModel):
    id: int
    channel_name: str

class Article(ArticleCreate):
    id: int
    word_count: int

    class Config:
        orm_mode = True
