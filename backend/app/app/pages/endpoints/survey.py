from fastapi import APIRouter, Request, Depends

from app.api.utils.security import get_current_user
from app.pages.utils.jinja import templates

router = APIRouter()


@router.get("/survey/category")
def survey_type(request: Request, user=Depends(get_current_user)):
    return templates.TemplateResponse("category.html",
                                      {
                                          "request": request,
                                          "user": user
                                      })
