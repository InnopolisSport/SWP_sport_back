import logging

import psycopg2.errors
from fastapi import APIRouter, Depends, responses, status
from sqlalchemy.orm import Session

from app.api.utils.db import get_db
from app.api.utils.security import get_current_user
from app.db.crud_enrolled import is_enrolled_anywhere, reenroll_student
from app.db.crud_users import find_student
from app.models.enrolled import EnrollRequest
from app.models.user import TokenUser

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

router = APIRouter()


@router.post("/enroll")
def enroll(enroll_req: EnrollRequest, db: Session = Depends(get_db),
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
