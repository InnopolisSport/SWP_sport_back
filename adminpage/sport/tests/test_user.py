import pytest
from django.contrib.auth.models import User
from django.core.management import call_command

from sport.fixtures.user_creation import *
from sport.models import Student

@pytest.mark.django_db
def test_student_create(user_factory):
    user = user_factory("A")
    group = Group.objects.get_or_create(
        verbose_name = "Students",
        name="S-1-5-21-721043115-644155662-3522934251-2285",
    )
    user.groups.add(group)
    assert User.objects.count() == 1
    assert Student.objects.count() == 1

# def test_student_delete(db, student_factory):
#     call_command("loaddata", "sport/fixtures/001_created_student.json")
    
#     assert User.objects.count() == 1
#     assert Student.objects.count() == 1