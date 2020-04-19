from fastapi import APIRouter, Request, Depends, responses

from app.utils.jinja import templates
from app.utils.security import get_current_user_optional

router = APIRouter()


@router.get("/login")
def login_page(request: Request,
               current_user: dict = Depends(get_current_user_optional)):
    if current_user is not None:
        return responses.RedirectResponse(url='/profile')

    return templates.TemplateResponse("login.html", {"request": request})
