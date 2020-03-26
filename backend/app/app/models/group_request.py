from enum import Enum
from datetime import datetime
from .base import Base


class RequestType(int, Enum):
    GROUP_ENROLL = 0
    GROUP_LEAVE = 1


class RequestStatus(int, Enum):
    OPEN = 0
    ACCEPTED = 1
    REJECTED = 2


class GroupRequest(Base):
    id: int
    group_id: int
    student_id: int
    created: datetime
    status: RequestStatus
    type: RequestType
    last_update: datetime
