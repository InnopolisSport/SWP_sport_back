import logging

from fastapi import APIRouter, Depends, responses
from fastapi.params import Path

from app.db import toggle_illness, find_student, get_detailed_hours
from app.models.user import TokenUser
from app.utils.db import get_db
from app.utils.security import get_current_user
from app.utils.tz import convert_from_utc

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

router = APIRouter()


@router.post("/sick/toggle")
def toggle_sick(db=Depends(get_db), user: TokenUser = Depends(get_current_user)):
    if user.is_student():
        student = find_student(db, user.email)
        toggle_illness(db, student.id)

        return responses.JSONResponse(status_code=200, content={
            "ok": True,
        })
    return responses.JSONResponse(status_code=200, content={
        "ok": False,
        "error": {
            "code": 1,
            "description": "You are not a student",
        }
    })


@router.get("/history/{semester_id}")
def history_semester(db=Depends(get_db),
                     user: TokenUser = Depends(get_current_user),
                     semester_id: int = Path(..., gt=0)):
    if user.is_student():
        student = find_student(db, user.email)
        trainings = get_detailed_hours(db, student.id, semester_id)
        return responses.JSONResponse(status_code=200, content={
            "trainings": list(map(lambda x: {
                "group": x.group,
                "timestamp": str(convert_from_utc(x.timestamp)),
                "hours": x.hours
            }, trainings))
        })
    return responses.JSONResponse(status_code=200, content={
        "ok": False,
        "error": {
            "code": 1,
            "description": "You are not a student",
        }
    })
