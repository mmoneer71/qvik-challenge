from fastapi import FastAPI

from app import __version__
from app.channels.router import channels_router
from app.articles.router import articles_router
from app.router import api_router
from app.const import COMMON_PREFIX

app = FastAPI(
    version=__version__,
    title="Application API",
    description="Application API for Qvik Backend challenge",
)



app.include_router(api_router)
app.include_router(articles_router, prefix=COMMON_PREFIX, tags=["Articles"])
app.include_router(channels_router, prefix=COMMON_PREFIX, tags=["Channels"])
