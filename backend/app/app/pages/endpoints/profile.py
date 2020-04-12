import logging

from fastapi import APIRouter, Request, Depends, responses

from app.api.utils.db import get_db
from app.api.utils.security import get_current_user_optional
from app.db import get_student_main_group, find_student, get_ongoing_semester
from app.pages.utils.jinja import templates

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

router = APIRouter()


@router.get("/profile")
def login_page(request: Request,
               db=Depends(get_db),
               current_user: dict = Depends(get_current_user_optional)):
    if current_user is not None:
        student_id = find_student(db, current_user.email).id
        group = get_student_main_group(db, student_id)
        sport_group = group.qualified_name if group is not None else None
        semester = get_ongoing_semester(db)
        return templates.TemplateResponse("profile.html", {
            "semester_name": semester.name,
            "enroll_open": semester.is_enroll_open,
            "request": request,
            "user": current_user,
            "sport_group": sport_group
        })

    return responses.RedirectResponse(url='/login')
