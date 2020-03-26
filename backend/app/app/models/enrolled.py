from pydantic import Field

from .base import Base


class EnrolledStudent(Base):
    group_id: int
    student_id: int


class EnrollRequest(Base):
    group_id: int = Field(..., gt=0)
