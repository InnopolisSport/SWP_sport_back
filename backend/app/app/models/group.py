from .base import Base


class Group(Base):
    id: int
    name: str
    sport_name: str
    trainer_id: int = None
