from fastapi import APIRouter, Request, Depends, responses, status

from app.api.utils.security import get_current_user_optional
from app.pages.utils.jinja import templates

router = APIRouter()


@router.get("/profile")
def login_page(request: Request,
               current_user: dict = Depends(get_current_user_optional)):
    if current_user is not None:
        return templates.TemplateResponse("profile.html", {"request": request, "user": current_user})

    return responses.RedirectResponse(url='/login')
