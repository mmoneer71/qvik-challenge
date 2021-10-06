from pydantic import BaseModel


class Message(BaseModel):
    message: str


class ChannelCreate(BaseModel):
    name: str

class Channel(ChannelCreate):
    id: int

    class Config:
        orm_mode = True


class Article(BaseModel):
    id: int
    url: str
    channel_id: int

    class Config:
        orm_mode = True
