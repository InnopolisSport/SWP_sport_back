from fastapi import APIRouter, Request, Depends

from app.api.utils.security import get_current_user
from app.db import get_sports
from app.pages.utils.db import get_db
from app.pages.utils.jinja import templates

router = APIRouter()


@router.get("/survey/category")
def survey_type(request: Request, user=Depends(get_current_user), db=Depends(get_db)):
    sports = get_sports(db)
    return templates.TemplateResponse("category.html",
                                      {
                                          "request": request,
                                          "user": user,
                                          "sports": sports,
                                      })
