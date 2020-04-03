from typing import Optional

from .base import Base


class Group(Base):
    id: int
    name: str
    sport_name: str
    semester: str
    capacity: int
    description: Optional[str] = ''
    trainer_id: Optional[int] = None

    @property
    def qualified_name(self):
        return f'{self.name} ({self.sport_name})'
