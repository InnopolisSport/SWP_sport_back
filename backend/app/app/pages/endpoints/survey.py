from fastapi import APIRouter, Request, Depends
from app.pages.utils.jinja import templates
from app.pages.utils.db import get_db
from app.db.crud_groups import get_sports

router = APIRouter()


@router.get("/survey")
def survey_page(request: Request, db=Depends(get_db)):
    return templates.TemplateResponse("survey.html",
                                      {
                                          "request": request,
                                          "sports": get_sports(),
                                          "user": {
                                              "name": "MYNAME",
                                              "surname": "MYSURNAME"
                                          }
                                      }
                                      )
