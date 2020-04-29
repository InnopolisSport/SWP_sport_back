import logging

import psycopg2.errors
from fastapi import APIRouter, Depends, responses, status

from app.db import get_ongoing_semester
from app.db.crud_enrolled import enroll_student_to_primary_group, enroll_student_to_secondary_group, unenroll_student
from app.db.crud_users import find_student
from app.models.group import EnrollRequest
from app.models.user import TokenUser
from app.utils.db import get_db
from app.utils.security import get_current_user

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

router = APIRouter()


@router.post("/enroll")
def enroll(enroll_req: EnrollRequest, db=Depends(get_db),
           user: TokenUser = Depends(get_current_user)):
    group_id = enroll_req.group_id
    if not user.is_student():
        return responses.JSONResponse(status_code=status.HTTP_200_OK, content={
            "ok": False,
            "error": {
                "description": "Not a student account",
                "code": 3,
            }
        })

    student_id = find_student(db, user.email).id
    if get_ongoing_semester(db).is_enroll_open:
        try:
            enroll_student_to_primary_group(db, group_id, student_id)
        except psycopg2.errors.RaiseException as e:
            return responses.JSONResponse(status_code=status.HTTP_200_OK, content={
                "ok": False,
                "error": {
                    "description": "Group you have chosen already full",
                    "code": 2,
                }
            })
    else:
        try:
            enroll_student_to_secondary_group(db, group_id, student_id)
        except psycopg2.errors.RaiseException as e:
            if 'too much groups' not in str(e):
                return responses.JSONResponse(status_code=status.HTTP_200_OK, content={
                    "ok": False,
                    "error": {
                        "description": "Group you have chosen already full",
                        "code": 2,
                    }
                })
            return responses.JSONResponse(status_code=status.HTTP_200_OK, content={
                "ok": False,
                "error": {
                    "description": "Too much secondary groups",
                    "code": 3,
                }
            })
    return responses.JSONResponse(status_code=status.HTTP_200_OK, content={
        "ok": True
    })


@router.post("/unenroll")
def unenroll(enroll_req: EnrollRequest, db=Depends(get_db),
             user: TokenUser = Depends(get_current_user)):
    group_id = enroll_req.group_id
    if not user.is_student():
        return responses.JSONResponse(status_code=status.HTTP_200_OK, content={
            "ok": False,
            "error": {
                "description": "Not a student account",
                "code": 3,
            }
        })

    student_id = find_student(db, user.email).id
    unenroll_student(db, group_id, student_id)
    return responses.JSONResponse(status_code=status.HTTP_200_OK, content={
        "ok": True
    })
