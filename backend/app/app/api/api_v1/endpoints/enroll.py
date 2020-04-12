import logging

import psycopg2.errors
from fastapi import APIRouter, Depends, responses, status

from app.api.utils.db import get_db
from app.api.utils.security import get_current_user
from app.db import get_ongoing_semester
from app.db.crud_enrolled import reenroll_student, get_enrollment_mapping
from app.db.crud_users import find_student
from app.models.group import EnrollRequest
from app.models.user import TokenUser

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

router = APIRouter()


@router.post("/enroll")
def enroll(enroll_req: EnrollRequest, db=Depends(get_db),
           user: TokenUser = Depends(get_current_user)):
    group_id = enroll_req.group_id
    if not user.is_student():
        return responses.JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={
            "ok": False,
            "error": {
                "description": "Not a student account",
                "code": 3,
            }
        })
    if not get_ongoing_semester(db).is_enroll_open:
        return responses.JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={
            "ok": False,
            "error": {
                "description": "Self enroll for current semester is already closed",
                "code": 4,
            }
        })

    student_id = find_student(db, user.email).id
    try:
        reenroll_student(db, group_id, student_id)
    except psycopg2.errors.RaiseException as e:
        return responses.JSONResponse(status_code=status.HTTP_200_OK, content={
            "ok": False,
            "error": {
                "description": "Group you have chosen already full",
                "code": 2,
            }
        })
    return responses.JSONResponse(status_code=status.HTTP_200_OK, content={
        "ok": True
    })


@router.get('/export_enroll')
def export_enroll(db=Depends(get_db), user: TokenUser = Depends(get_current_user)):
    if not user.is_admin():
        return responses.JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={
            "ok": False,
            "error": {
                "description": "Only admin can view enrollment mapping",
                "code": 1
            }
        })
    # TODO: export as a file
    return get_enrollment_mapping(db)
