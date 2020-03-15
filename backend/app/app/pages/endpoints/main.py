from fastapi import APIRouter, Request, Cookie
from app.pages.utils.jinja import templates

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

router = APIRouter()


@router.get("/")
def index_page(request: Request, access_token: str = Cookie(None)):
    logger.debug(f"\n\n{access_token is not None}\n\n")
    return templates.TemplateResponse("login.html", {"request": request, "logged_in": access_token is not None})
