from typing import Optional, List

from pydantic import Field

from .base import Base
from app.core.config import BACHELOR_PREFIX


class TokenUser(Base):
    first_name: str
    last_name: str
    email: str
    groups: List[str]
    role: Optional[str] = Field(..., description="A study group in format B18-02 if any or None")

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def in_group(self, group: str) -> bool:
        return group in self.groups

    def is_student(self) -> bool:
        return self.in_group("Students") and self.role.startswith(BACHELOR_PREFIX)

    def is_trainer(self) -> bool:
        return self.in_group("Школа физической активности для здоровья")

    def is_admin(self) -> bool:
        # TODO: clarify admin tag
        return self.in_group("Student Affairs and Development Office")


class BaseUser(Base):
    id: int
    first_name: str
    last_name: str
    email: str

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Trainer(BaseUser):
    pass


class Student(BaseUser):
    is_ill: bool


class Admin(BaseUser):
    pass
