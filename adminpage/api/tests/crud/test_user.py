import pytest
from django.contrib.auth.models import User

from sport.models import Student
from api.crud import get_email_name_like_students


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


@pytest.mark.django_db
def test_get_email_name_like_students(student_factory):
    user = student_factory(username="a", first_name="Kirill", last_name="Fedoseev", email="k.fedoseev@innopolis.university")
    assert get_email_name_like_students("Kirill") == [{
        "id": user.student.pk,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email
    }]
    assert len(get_email_name_like_students("Kir")) == 1
    assert len(get_email_name_like_students("Kirill Fed")) == 1
    assert len(get_email_name_like_students("Kirill Fedoseev")) == 1
    assert len(get_email_name_like_students("k.fedoseev")) == 1
    assert len(get_email_name_like_students("k.fedoseev@innopolis.university")) == 1
    assert len(get_email_name_like_students("kfedoseev")) == 0
