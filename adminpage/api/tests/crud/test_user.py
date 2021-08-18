from datetime import date

import pytest
from django.contrib.auth import get_user_model

from sport.models import Student, Group
from sport.models import MedicalGroups
from api.crud import get_email_name_like_students


User = get_user_model()


@pytest.mark.django_db
def test_student_create(student_factory):
    student_factory("A@foo.bar")
    assert User.objects.count() == 1
    assert Student.objects.count() == 1


@pytest.mark.django_db
def test_student_delete(student_factory):
    student_user = student_factory("A@foo.bar")
    assert User.objects.count() == 1
    assert Student.objects.count() == 1
    student_user.delete()
    assert User.objects.count() == 0
    assert Student.objects.count() == 0


@pytest.mark.django_db
def test_get_email_name_like_students(
        student_factory,
        semester_factory,
        sport_factory,
        group_factory
):
    start = date(2020, 1, 20)
    end = date(2020, 1, 27)
    sem = semester_factory(
        name="S20",
        start=start,
        end=end,
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
    )
    group.allowed_medical_groups.set([
        MedicalGroups.NO_CHECKUP,
        MedicalGroups.PREPARATIVE,
        MedicalGroups.SPECIAL1,
        MedicalGroups.SPECIAL2,
        MedicalGroups.GENERAL
    ])
    user = student_factory(
        first_name="Kirill",
        last_name="Fedoseev",
        email="k.fedoseev@innopolis.university",
    )
    user.student.sport = sport
    user.student.save()

    assert get_email_name_like_students(group.id, "Kirill") == [{
        "id": user.student.pk,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "full_name": f"{user.first_name} {user.last_name}",
    }]
    assert len(get_email_name_like_students(group.id, "Kir")) == 1
    assert len(get_email_name_like_students(group.id, "Kirill Fed")) == 1
    assert len(get_email_name_like_students(group.id, "Kirill Fedoseev")) == 1
    assert len(get_email_name_like_students(group.id, "k.fedoseev")) == 1
    assert len(
        get_email_name_like_students(group.id,"k.fedoseev@innopolis.university")
    ) == 1
    assert len(get_email_name_like_students(group.id, "kfedoseev")) == 0

