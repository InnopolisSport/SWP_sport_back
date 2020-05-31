import uuid
from typing import List, Optional

import pytest
from django.contrib.auth.models import(
     User, Group, Permission
)

@pytest.fixture
@pytest.mark.django_db
def student_group() -> Group:
    group = Group.objects.get_or_create(
        verbose_name = "Students",
        name="S-1-5-21-721043115-644155662-3522934251-2285",
    )
    return group

def create_user_in_groups(
    predefined_groups: Optional[List[Group]] = [],
):
    def create_app_user(
        username: str,
        password: Optional[str] = None,
        first_name: Optional[str] = "first name",
        last_name: Optional[str] = "last name",
        email: Optional[str] = "foo@bar.com",
        is_staff: str = False,
        is_superuser: str = False,
        is_active: str = True,
        groups: List[Group] = [],
    ) -> User:
        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email,
            is_staff=is_staff,
            is_superuser=is_superuser,
            is_active=is_active,
        )
        user.groups.add(*groups)
        user.groups.add(*predefined_groups)
        return user
    return create_app_user

@pytest.fixture
@pytest.mark.django_db
def user_factory():
    return create_user_in_groups()

@pytest.fixture
@pytest.mark.django_db
def student_factory(student_group):
    return create_user_in_groups(
        predefined_groups = [student_group]
    )
