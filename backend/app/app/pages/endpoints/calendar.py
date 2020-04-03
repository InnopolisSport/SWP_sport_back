from fastapi import APIRouter, Request, Depends, HTTPException, Path

from app.api.utils.security import get_current_user
from app.db.crud_groups import get_sport_by_id
from app.pages.utils.db import get_db
from app.pages.utils.jinja import templates

router = APIRouter()


@router.get("/calendar/{sport_id}")
def login_page(request: Request, user=Depends(get_current_user), conn=Depends(get_db),
               sport_id: int = Path(..., gt=0)):
    sport = get_sport_by_id(conn, sport_id)
    if sport is None:
        raise HTTPException(status_code=404, detail=f"Sport with id {sport_id} was not found")
    else:
        return templates.TemplateResponse("calendar.html",
                                          {
                                              "request": request,
                                              "sport": sport,
                                              "user": user
                                          })
