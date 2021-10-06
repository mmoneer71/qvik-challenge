from fastapi import APIRouter

from app.database import Base, engine
from app.schemas import Message
from app.samples import sample_index_message
from app.service import get_sample_index

api_router = APIRouter()

Base.metadata.create_all(bind=engine)

@api_router.get(
    "/",
    tags=["Index"],
    responses={
        200: {
            "model": Message,
            "description": "So, it works!",
            "content": {"application/json": {"example": sample_index_message}},
        }
    },
)
async def index() -> Message:
    return get_sample_index()
