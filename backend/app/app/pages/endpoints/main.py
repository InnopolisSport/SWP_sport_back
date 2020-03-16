import logging

from fastapi import APIRouter, Request, Depends

from app.api.utils.security import get_current_user_optional
from app.pages.utils.jinja import templates

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

router = APIRouter()


@router.get("/")
def index_page(request: Request,
               current_user: dict = Depends(get_current_user_optional)
               ):
    return templates.TemplateResponse("login.html", {"request": request,
                                                     "user": current_user
                                                     }
                                      )
