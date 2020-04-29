from typing import Optional

from pydantic import Field

from .base import Base


class Group(Base):
    id: int
    name: str
    sport_name: str
    semester: str
    capacity: int
    description: Optional[str] = ''
    trainer_id: Optional[int] = None
    is_club: bool

    @property
    def qualified_name(self):
        return f'{self.name} ({self.sport_name})'


class EnrolledGroup(Group):
    is_primary: bool


class EnrollRequest(Base):
    group_id: int = Field(..., gt=0)
