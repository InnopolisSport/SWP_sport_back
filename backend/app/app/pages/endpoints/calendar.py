from fastapi import APIRouter, Request, Depends, Query

from app.api.utils.security import get_current_user
from app.pages.utils.jinja import templates

router = APIRouter()


@router.get("/calendar")
def login_page(request: Request, user=Depends(get_current_user),
               sport_id: int = Query(..., gt=0), sport_name: str = Query(..., min_length=1)):
    return templates.TemplateResponse("calendar.html",
                                      {
                                          "request": request,
                                          "sport": {
                                              "id": sport_id,
                                              "name": sport_name
                                          },
                                          "user": user
                                      })
