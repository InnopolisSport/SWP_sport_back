import unittest
from datetime import date

import pytest
from django.utils import timezone

from api.crud import enroll_student, unenroll_student, get_primary_groups, \
    get_ongoing_semester
from sport.models import Enroll

dummy_date = date(2020, 1, 1)
assertMembers = unittest.TestCase().assertCountEqual


@pytest.mark.django_db
def test_primary_group_export(
        student_factory,
        sport_factory,
        semester_factory,
        group_factory,
        training_factory,
        attendance_factory,
):
    student = student_factory("A").student
    sport = sport_factory(name="Sport")
    s1 = semester_factory(name="S19", start=dummy_date, end=dummy_date)
    g1 = group_factory(name="G11", sport=sport, semester=s1, capacity=20)
    g2 = group_factory(name="G12", sport=sport, semester=s1, capacity=20)

    trainings = []
    for i, g in enumerate([g1, g2, ]):
        t = training_factory(group=g, start=timezone.now(), end=timezone.now())
        trainings.append(t)
        attendance_factory(training=t, student=student, hours=i + 1)
    # g1 - 1 hour,
    # g2 - 2 hours

    primary_groups = get_primary_groups(get_ongoing_semester().pk)
    assertMembers(
        primary_groups,
        {
            student.pk: g2.pk,
        }
    )


@pytest.mark.django_db
def test_primary_group_export_same_hours(
        student_factory,
        sport_factory,
        semester_factory,
        group_factory,
        training_factory,
        attendance_factory,
):
    student = student_factory("A").student
    sport = sport_factory(name="Sport")
    s1 = semester_factory(name="S19", start=dummy_date, end=dummy_date)
    g1 = group_factory(name="G11", sport=sport, semester=s1, capacity=20)
    g2 = group_factory(name="G12", sport=sport, semester=s1, capacity=20)

    trainings = []
    for i, g in enumerate([g1, g2, ]):
        t = training_factory(group=g, start=timezone.now(), end=timezone.now())
        trainings.append(t)
        attendance_factory(training=t, student=student, hours=2)

    primary_groups = get_primary_groups(get_ongoing_semester().pk)
    assert len(primary_groups) == 1
