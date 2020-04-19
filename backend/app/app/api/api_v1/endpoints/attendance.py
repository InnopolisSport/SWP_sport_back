import logging

from fastapi import APIRouter, Depends

from app.api.utils.db import get_db
from app.db import mark_hours, clean_students_id
from app.models.attendance import MarkAttendanceRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

router = APIRouter()


@router.post("/mark/")
def mark_attendance(data: MarkAttendanceRequest, db=Depends(get_db)):
    """
    Put hours for training session for give students. Update hours if student already has hours for training
    """
    cleaned_students = clean_students_id(db, tuple(data.students_hours.keys()))
    hours_to_mark = [(s.id, data.students_hours[s.id]) for s in cleaned_students]
    mark_hours(db, data.training_id, hours_to_mark)
    return hours_to_mark
