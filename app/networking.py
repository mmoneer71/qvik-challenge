from fastapi import FastAPI

from app import __version__
from app.router import api_router

app = FastAPI(
    version=__version__,
    title="Application API",
    description="Application API for Qvik Backend challenge",
)

app.include_router(api_router)
