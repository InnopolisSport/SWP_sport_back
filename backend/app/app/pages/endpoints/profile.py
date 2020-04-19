import logging

from fastapi import APIRouter, Request, Depends, responses

from app.api.utils.db import get_db
from app.api.utils.security import get_current_user_optional
from app.db import get_student_groups, find_student, get_ongoing_semester, get_brief_hours
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
        groups = get_student_groups(db, student_id)
        sport_groups = list(map(lambda group: group.qualified_name, groups))
        semester = get_ongoing_semester(db)

        return templates.TemplateResponse("profile.html", {
            "request": request,
            "user": current_user,
            "common": {
                "semester_name": semester.name,
                "enroll_open": semester.is_enroll_open,
            },
            "student": {
                "student_id": student_id,
                "sport_groups": sport_groups,
                **(student.dict())
            },
            "semesters": get_brief_hours(db, student_id)
        })

    return responses.RedirectResponse(url='/login')
