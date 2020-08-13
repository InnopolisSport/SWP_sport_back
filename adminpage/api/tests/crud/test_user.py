from datetime import date

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
def test_get_email_name_like_students(student_factory, semester_factory, sport_factory, group_factory):
    user = student_factory(username="a", first_name="Kirill", last_name="Fedoseev", email="k.fedoseev@innopolis.university")
    assert get_email_name_like_students(0, "Kirill") == [{
        "id": user.student.pk,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "full_name": f"{user.first_name} {user.last_name}",
    }]
    assert len(get_email_name_like_students(0, "Kir")) == 1
    assert len(get_email_name_like_students(0, "Kirill Fed")) == 1
    assert len(get_email_name_like_students(0, "Kirill Fedoseev")) == 1
    assert len(get_email_name_like_students(0, "k.fedoseev")) == 1
    assert len(get_email_name_like_students(0, "k.fedoseev@innopolis.university")) == 1
    assert len(get_email_name_like_students(0, "kfedoseev")) == 0

    start = date(2020, 1, 20)
    end = date(2020, 1, 27)
    choice_deadline = date(2020, 1, 27)
    sem = semester_factory(
        name="S20",
        start=start,
        end=end,
        choice_deadline=choice_deadline,
    )

    sport = sport_factory(
        name="football",
        special=False,
    )

    group = group_factory(
        name="F-S20-01",
        capacity=30,
        sport=sport,
        semester=sem,
        minimum_medical_group_id=None
    )
    assert len(get_email_name_like_students(group.id, "k.fedoseev@innopolis.university")) == 1
    group.minimum_medical_group_id = 0
    group.save()
    assert len(get_email_name_like_students(group.id, "k.fedoseev@innopolis.university")) == 0
    user.student.medical_group_id = 0
    user.save()
    assert len(get_email_name_like_students(group.id, "k.fedoseev@innopolis.university")) == 1
