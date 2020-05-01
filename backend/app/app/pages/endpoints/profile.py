import logging

from fastapi import APIRouter, Request, Depends, responses

from app.db import get_student_groups, find_student, get_ongoing_semester, get_brief_hours, find_trainer, \
    get_training_groups
from app.models.user import TokenUser
from app.utils.auth import logout
from app.utils.db import get_db
from app.utils.jinja import templates
from app.utils.security import get_current_user_optional

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

router = APIRouter()


@router.get("/profile")
def login_page(request: Request,
               db=Depends(get_db),
               current_user: TokenUser = Depends(get_current_user_optional)):
    logger.debug(f"\n\n{request.url.components}\n\n")
    if current_user is not None:
        student = find_student(db, current_user.email)
        trainer = find_trainer(db, current_user.email)
        if student is None:
            return logout('/profile')
        student_id = student.id
        groups = get_student_groups(db, student_id)
        sport_groups = list(map(lambda group: {
            'id': group.id,
            'is_primary': group.is_primary,
            'name': group.qualified_name
        }, groups))
        semester = get_ongoing_semester(db)

        training_groups = get_training_groups(db, trainer.id) if trainer is not None else None

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
                "semesters": get_brief_hours(db, student_id),
                **(student.dict())
            },
            "trainer": {
                "sport_groups": training_groups,
                **(trainer.dict() if trainer is not None else {})
            }
        })

    return responses.RedirectResponse(url='/login')
