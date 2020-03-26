from typing import Optional, List

from pydantic import Field

from .base import Base


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
        return self.groups.__contains__(group)

    def is_student(self) -> bool:
        return self.in_group("Students")


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
    pass


class Admin(BaseUser):
    pass
