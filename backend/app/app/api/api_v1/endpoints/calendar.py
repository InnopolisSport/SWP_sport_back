import logging
from datetime import datetime
from typing import Tuple, Optional

from fastapi import APIRouter, Depends, Path, Query, responses, status

from app.api.utils.db import get_db
from app.api.utils.security import get_current_user
from app.api.utils.tz import convert_from_utc
from app.db import find_student, find_trainer, Training
from app.db.crud_groups import get_current_load
from app.db.crud_training import get_trainings_in_time, get_trainings_for_student, get_trainings_for_trainer
from app.models.user import TokenUser

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

router = APIRouter()


def convert_training(db, t: Tuple[str, datetime, datetime, int, int]) -> dict:
    title, start, end, capacity, group_id = t
    return {
        "title": title,
        "start": convert_from_utc(start),
        "end": convert_from_utc(end),
        "extendedProps": {
            "capacity": capacity,
            # TODO: n+1 problem?
            "currentLoad": get_current_load(db, group_id),
            "id": group_id
        }
    }


def convert_training_profile(t: Training) -> dict:
    return {
        "title": t.group_name,
        "start": convert_from_utc(t.start),
        "end": convert_from_utc(t.end),
        "extendedProps": {
            "id": t.id,
            "can_grade": t.can_grade
        }
    }


@router.get("/{sport_id}/schedule")
def get_schedule(db=Depends(get_db), *, sport_id: int = Path(..., gt=0), start: datetime, end: datetime,
                 timezone: Optional[str] = Query(None, alias="timeZone")):
    trainings = get_trainings_in_time(db, sport_id, start, end)
    return list(map(lambda training: convert_training(db, training), trainings))


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
