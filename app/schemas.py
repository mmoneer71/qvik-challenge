from pydantic import BaseModel


class Message(BaseModel):
    message: str


class Channel(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class Article(BaseModel):
    id: int
    url: str
    channel_id: int

    class Config:
        orm_mode = True
