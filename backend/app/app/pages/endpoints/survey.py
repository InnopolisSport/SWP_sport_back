from fastapi import APIRouter, Request, Depends

from app.api.utils.security import get_current_user
from app.db import get_sports, get_groups, get_current_load, get_sc_training_group
from app.pages.utils.db import get_db
from app.pages.utils.jinja import templates

router = APIRouter()


@router.get("/survey/category")
def survey_type(request: Request, user=Depends(get_current_user), db=Depends(get_db)):
    sports = get_sports(db)
    # TODO: n+1 problem?
    clubs = [club for club in get_groups(db, clubs=True) if get_current_load(db, club.id) < club.capacity]
    sc_training_group_id = get_sc_training_group(db).id
    return templates.TemplateResponse("category.html",
                                      {
                                          "request": request,
                                          "user": user,
                                          "sports": sports,
                                          "clubs": clubs,
                                          "sc_training_group_id": sc_training_group_id
                                      })
