import logging
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Path, Query, responses, status

from app.db import find_student, find_trainer, Training
from app.db.crud_training import get_trainings_in_time, get_trainings_for_student, get_trainings_for_trainer
from app.models.user import TokenUser
from app.utils.db import get_db
from app.utils.security import get_current_user
from app.utils.tz import convert_from_utc

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

router = APIRouter()


def convert_training(t: Training) -> dict:
    return {
        "title": t.group_name,
        "start": convert_from_utc(t.start),
        "end": convert_from_utc(t.end),
        "extendedProps": {
            "id": t.id,
            "group_id": t.group_id,
            "training_class": t.training_class,
            "current_load": t.current_load,
            "capacity": t.capacity
        }
    }


def convert_training_profile(t: Training) -> dict:
    return {
        "title": t.group_name,
        "start": convert_from_utc(t.start),
        "end": convert_from_utc(t.end),
        "extendedProps": {
            "id": t.id,
            "group_id": t.group_id,
            "can_grade": t.can_grade,
            "training_class": t.training_class
        }
    }


@router.get("/{sport_id}/schedule")
def get_schedule(db=Depends(get_db), *, sport_id: int = Path(..., gt=0), start: datetime, end: datetime,
                 timezone: Optional[str] = Query(None, alias="timeZone")):
    trainings = get_trainings_in_time(db, sport_id, start, end)
    return list(map(convert_training, trainings))


@router.get("/trainings")
def get_student_trainings(db=Depends(get_db),
                          *,
                          start: datetime,
                          end: datetime,
                          user: TokenUser = Depends(get_current_user)):
    if not user.is_student() and not user.is_trainer():
        return responses.JSONResponse(status_code=status.HTTP_200_OK, content={
            "ok": False,
            "error": {
                "description": "Neither a student account nor a trainer.",
                "code": 3,
            }
        })

    student_trainings = []
    trainer_trainings = []
    if user.is_student():
        student = find_student(db, user.email)
        student_trainings = get_trainings_for_student(db, student.id, start, end)

    trainer = find_trainer(db, user.email)
    if trainer is not None:
        trainer_trainings = get_trainings_for_trainer(db, trainer.id, start, end)

    return list(map(convert_training_profile, set(trainer_trainings + student_trainings)))
