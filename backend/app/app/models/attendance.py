from datetime import datetime, date
from typing import Dict

from pydantic import PositiveInt

from .base import Base


class AttendanceTraining(Base):
    group: str
    timestamp: datetime
    hours: float


class AttendanceSemester(Base):
    semester_id: int
    semester_name: str
    semester_start: date
    semester_end: date
    hours: float


class MarkAttendanceRequest(Base):
    training_id: PositiveInt
    students_hours: Dict[PositiveInt, float]

    class Config:
        schema_extra = {
            "example": {
                "training_id": 5,
                "students_hours": {
                    "1": 1.0,
                    "42": 1.5,
                },
            }
        }
