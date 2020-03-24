from .base import Base


class GroupRequest(Base):
    id: int
    group_id: int
    student_id: int
    created_timestamp: str
    status: int
    last_updated: str
