import pytest
from django.contrib.auth.models import User

from sport.models import Student


@pytest.mark.django_db
def test_student_create(student_factory):
    student_factory("A")
    assert User.objects.count() == 1
    assert Student.objects.count() == 1


@pytest.mark.django_db
def test_student_delete(student_factory):
    student_user = student_factory("A")
    assert User.objects.count() == 1
    assert Student.objects.count() == 1
    student_user.delete()
    assert User.objects.count() == 0
    assert Student.objects.count() == 0
