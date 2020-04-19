from datetime import datetime
from operator import eq

from .base import Base


class Training(Base):
    id: int
    start: datetime
    end: datetime
    group_name: str
    can_grade: bool = False

    def __hash__(self):
        fields = [self.id, self.start, self.end, self.group_name]
        return sum(map(hash, fields))

    def __eq__(self, other):
        """
        Equality here ignores can_grade param

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
