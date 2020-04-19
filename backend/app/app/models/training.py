from datetime import datetime
from typing import Optional

from .base import Base


class Training(Base):
    id: int
    start: datetime
    end: datetime
    group_name: str
    can_grade: Optional[bool] = False
