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


# Shared properties
class UserBase(Base):
    email: Optional[str] = None
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    full_name: Optional[str] = None


class UserBaseInDB(UserBase):
    id: int = None


# Properties to receive via API on creation
class UserCreate(UserBaseInDB):
    email: str
    password: str


# Properties to receive via API on update
class UserUpdate(UserBaseInDB):
    password: Optional[str] = None


# Additional properties to return via API
class User(UserBaseInDB):
    pass


# Additional properties stored in DB
class UserInDB(UserBaseInDB):
    hashed_password: str
