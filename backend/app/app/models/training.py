from datetime import datetime

from .base import Base


class Training(Base):
    id: int
    start: datetime
    end: datetime
    group_id: int
