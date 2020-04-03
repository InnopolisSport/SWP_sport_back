import logging

from fastapi import APIRouter, Request, Depends, responses

from app.api.utils.security import get_current_user_optional
from app.pages.utils.jinja import templates

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

router = APIRouter()


@router.get("/profile")
def login_page(request: Request,
               current_user: dict = Depends(get_current_user_optional)):
    if current_user is not None:
        # sport_group = "G1"
        sport_group = None
        return templates.TemplateResponse("profile.html", {
            "request": request,
            "user": current_user,
            "sport_group": sport_group
        })

    return responses.RedirectResponse(url='/login')
