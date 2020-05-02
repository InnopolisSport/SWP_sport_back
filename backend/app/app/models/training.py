from datetime import datetime
from operator import eq
from typing import Optional

from .base import Base


class Training(Base):
    id: Optional[int] = None
    start: datetime
    end: datetime
    group_name: str
    can_grade: bool = False
    training_class: Optional[str] = None
    current_load: Optional[int] = None
    capacity: Optional[int] = None
    group_id: Optional[int] = None

    def __hash__(self):
        fields = [self.id, self.start, self.end, self.group_name]
        return sum(map(hash, fields))

    def __eq__(self, other):
        """
        WARNING!!!
        Equality here ignores can_grade param!

        :param other:
        :return:
        """
        if type(other) != Training:
            raise ValueError(f"Can't compare training with {type(other)} else")

        fields = ["id", "start", "end", "group_name"]

        return all([eq(self.__getattribute__(field), other.__getattribute__(field)) for field in fields])


class TrainingInfo(Base):
    group_name: str
    start: datetime
    trainer_id: int


class TrainingGrade(Base):
    student_id: int
    full_name: str
    email: str
    hours: float
