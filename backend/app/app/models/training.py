from datetime import datetime
from typing import Optional

from .base import Base


class Training(Base):
    id: int
    start: datetime
    end: datetime
    group_name: str
    can_grade: Optional[bool] = False


class TrainingInfo(Base):
    group_name: str
    start: datetime
    trainer_id: int


class TrainingGrade(Base):
    student_id: int
    full_name: str
    email: str
    hours: float
