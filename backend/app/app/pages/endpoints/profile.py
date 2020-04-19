import logging

from fastapi import APIRouter, Request, Depends, responses

from app.api.utils.db import get_db
from app.api.utils.security import get_current_user_optional
from app.db import get_student_main_group, find_student, get_ongoing_semester, get_brief_hours
from app.models.user import TokenUser
from app.pages.utils.auth import logout
from app.pages.utils.jinja import templates

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

router = APIRouter()


@router.get("/profile")
def login_page(request: Request,
               db=Depends(get_db),
               current_user: TokenUser = Depends(get_current_user_optional)):
    if current_user is not None:
        student = find_student(db, current_user.email)
        if student is None:
            return logout('/profile')
        student_id = student.id
        group = get_student_main_group(db, student_id)
        sport_group = group.qualified_name if group is not None else None
        semester = get_ongoing_semester(db)

        student_hours = get_brief_hours(db, student_id)
        [hours] = [sem.hours for sem in student_hours if sem.semester_id == semester.id]

        return templates.TemplateResponse("profile.html", {
            "request": request,
            "user": current_user,
            "common": {
                "semester_name": semester.name,
                "enroll_open": semester.is_enroll_open,
            },
            "student": {
                "student_id": student_id,
                "sport_group": sport_group,
                "hours": hours,
                **(student.dict())
            },
            "semesters": get_brief_hours(db, student_id)
        })

    return responses.RedirectResponse(url='/login')
