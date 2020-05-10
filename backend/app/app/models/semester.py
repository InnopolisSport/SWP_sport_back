from datetime import date, timezone, datetime

from .base import Base


class Semester(Base):
    id: int
    name: str
    start: date
    end: date
    choice_deadline: date

    @property
    def is_enroll_open(self) -> bool:
        # db stores timestamps in the UTC format, so we need to use UTC timezone here
        return datetime.now(timezone.utc).date() <= self.choice_deadline
