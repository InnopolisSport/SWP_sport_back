from datetime import datetime

from .base import Base


class AttendanceTraining(Base):
    group: str
    timestamp: datetime
    hours: float


class AttendanceSemester(Base):
    semester_id: int
    semester_name: str
    hours: float
