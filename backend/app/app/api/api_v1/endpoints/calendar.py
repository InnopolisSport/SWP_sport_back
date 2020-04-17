import logging
from datetime import datetime
from typing import Tuple

from fastapi import APIRouter, Depends, Path

from app.api.utils.db import get_db
from app.api.utils.tz import convert_from_utc
from app.db.crud_groups import get_current_load
from app.db.crud_training import get_trainings_in_time

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


@router.get("/{sport_id}/schedule")
def get_schedule(db=Depends(get_db), *, sport_id: int = Path(..., gt=0), start: datetime, end: datetime):
    trainings = get_trainings_in_time(db, sport_id, start, end)
    return list(map(lambda training: convert_training(db, training), trainings))
