import logging
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, responses
from fastapi.params import Path, Query

from app.core.config import TRAINING_EDITABLE_DAYS
from app.db import mark_hours, clean_students_id, find_trainer, get_training_info, get_students_grades, Optional, \
    get_email_name_like_students
from app.models.attendance import MarkAttendanceRequest
from app.models.user import TokenUser
from app.utils.db import get_db
from app.utils.security import get_current_user
from app.utils.tz import convert_from_utc

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

router = APIRouter()


@router.get("/{training_id}/grades")
def mark_attendance(db=Depends(get_db),
                    user: TokenUser = Depends(get_current_user),
                    training_id: int = Path(..., gt=0)):
    trainer = find_trainer(db, user.email)
    training_info = get_training_info(db, training_id) if training_id is not None else None
    if trainer is None or training_info.trainer_id != trainer.id:
        return responses.JSONResponse(status_code=200, content={
            "ok": False,
            "error": {
                "code": 1,
                "description": "You are not a trainer for this group",
            }
        })
    return {
        "group_name": training_info.group_name,
        "start": training_info.start,
        "grades": get_students_grades(db, training_id)
    }


@router.post("/mark")
def mark_attendance(data: MarkAttendanceRequest,
                    db=Depends(get_db),
                    user: TokenUser = Depends(get_current_user)):
    """
    Put hours for training session for give students. Update hours if student already has hours for training
    """
    trainer = find_trainer(db, user.email)
    if trainer is None or get_training_info(db, data.training_id).trainer_id != trainer.id:
        return responses.JSONResponse(status_code=200, content={
            "ok": False,
            "error": {
                "code": 1,
                "description": "You are not a trainer for this group",
            }
        })
    training_info = get_training_info(db, data.training_id)
    now_time = convert_from_utc(datetime.utcnow())
    start_time = convert_from_utc(training_info.start)
    editing_interval = timedelta(days=TRAINING_EDITABLE_DAYS)
    if not start_time <= now_time <= start_time + editing_interval:
        return responses.JSONResponse(status_code=200, content={
            "ok": False,
            "error": {
                "code": 2,
                "description": "The training is not editable "
                               f"after {TRAINING_EDITABLE_DAYS} from start",
                "training_editable_days": TRAINING_EDITABLE_DAYS,
            },
        })
    max_hours = training_info.academic_duration
    cleaned_students = clean_students_id(db, tuple(data.students_hours.keys()))
    # hours_to_mark = [(s.id, min(max_hours, data.students_hours[s.id])) for s in cleaned_students]
    hours_to_mark = []
    negative_mark = []
    over_mark = []
    for student in cleaned_students:
        hours_put = data.students_hours[student.id]
        if hours_put < 0:
            negative_mark.append((student.email, hours_put))
        elif hours_put > max_hours:
            over_mark.append((student.email, hours_put))
        else:
            hours_to_mark.append((student.id, hours_put))
    if negative_mark or over_mark:
        return responses.JSONResponse(status_code=200, content={
            "ok": False,
            "error": {
                "code": 2,
                "description": "Some students obtained negative marks over overflowed maximum",
                "negative_marks": negative_mark,
                "overflow_mark": over_mark,
            },
        })
    else:
        mark_hours(db, data.training_id, hours_to_mark)
        return hours_to_mark


@router.get("/suggest_student")
def suggest_students(input_term: str = Query(..., alias="term"),
                     current_user: Optional[TokenUser] = Depends(get_current_user),
                     db=Depends(get_db)):
    if find_trainer(db, current_user.email) is not None:
        suggested_students = get_email_name_like_students(db, input_term)

        return [
            {
                "value": f"{student.id}_{student.full_name}_{student.email}",
                "label": f"{student.full_name} ({student.email})"
            }
            for student in
            suggested_students]

        # return [{"value": student.email, "label": f"{student.full_name} ({student.email})"} for student in
        #         suggested_students]
