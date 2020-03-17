from fastapi import FastAPI
from starlette.requests import Request

from app.api.api_v1.api import api_router
from app.core import config
from app.db.session import Session

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

app = FastAPI(title=config.PROJECT_NAME)

app.include_router(api_router, prefix=config.API_V1_STR)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next ):
    logger.debug("Entered middleware")
    request.state.db = Session()
    response = await call_next(request)
    request.state.db.close()
    return response

