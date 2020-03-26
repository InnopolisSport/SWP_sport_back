from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request

from app.api.api_v1.api import api_router
from app.pages.pages import pages_router
from app.core import config
from app.db import create_connection

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

app = FastAPI(title=config.PROJECT_NAME)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(pages_router)
app.include_router(api_router, prefix=config.API_V1_STR)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    logger.debug("Entered middleware")
    request.state.db = create_connection()
    response = await call_next(request)
    request.state.db.close()
    return response
