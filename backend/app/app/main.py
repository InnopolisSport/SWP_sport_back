import logging

from fastapi import FastAPI, status, responses
from fastapi.exception_handlers import http_exception_handler as default_http_exception_handler
from fastapi.exceptions import HTTPException
from starlette.requests import Request

from app.api.api_v1.api import api_router
from app.core import config
from app.db import create_connection
from app.pages.pages import pages_router

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

app = FastAPI(title=config.PROJECT_NAME)

app.include_router(pages_router)
app.include_router(api_router, prefix=config.API_V1_STR)

if config.DEBUG:
    from fastapi.staticfiles import StaticFiles

    app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.db = create_connection()
    response = await call_next(request)
    request.state.db.close()
    return response


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == status.HTTP_401_UNAUTHORIZED:
        url = str(request.url)
        if url.startswith(config.BASE_LOCAL_URL):
            url = config.BASE_URL + url[len(config.BASE_LOCAL_URL):]
        return responses.RedirectResponse(
            url=f"/api/login?state=login&redirect_uri={url}")

    else:
        return await default_http_exception_handler(request, exc)
