from .base import Base


class Training(Base):
    id: int
    start_timestamp: str
    end_timestamp: str
    group_id: int
