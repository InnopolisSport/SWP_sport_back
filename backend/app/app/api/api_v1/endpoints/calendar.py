import logging
from datetime import datetime
from typing import Tuple

from fastapi import APIRouter, Depends, Path

from app.api.utils.db import get_db
from app.db.crud_training import get_trainings_in_time

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

router = APIRouter()


def convert_training(t: Tuple[str, datetime, datetime, int, int]) -> dict:
    title, start, end, capacity, group_id = t
    return {
        "title": title,
        "start": start,
        "end": end,
        "extendedProps": {
            "capacity": capacity,
            "currentLoad": 5,
            "id": group_id
        }
    }


@router.get("/{sport_id}/schedule")
def get_schedule(db=Depends(get_db), *, sport_id: int = Path(..., gt=0), start: datetime, end: datetime):
    trainings = get_trainings_in_time(db, sport_id, start, end)
    return list(map(convert_training, trainings))
