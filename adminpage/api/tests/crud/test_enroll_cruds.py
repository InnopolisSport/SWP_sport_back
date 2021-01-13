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
def test_enroll(
        student_factory,
        sport_factory,
        semester_factory,
        group_factory
):
    student = student_factory("A").student
    sport = sport_factory(name="Sport")
    s1 = semester_factory(name="S19", start=dummy_date, end=dummy_date)
    s2 = semester_factory(name="S20", start=dummy_date, end=dummy_date)
    g11 = group_factory(name="G11", sport=sport, semester=s1, capacity=20)
    g12 = group_factory(name="G12", sport=sport, semester=s1, capacity=20)
    g2 = group_factory(name="G2", sport=sport, semester=s2, capacity=20)

    assert Enroll.objects.filter(student=student).count() == 0
    enroll_student(g11, student)
    assert Enroll.objects.filter(student=student).count() == 1
    enroll_student(g12, student)
    assert Enroll.objects.filter(student=student).count() == 2
    enroll_student(g2, student)
    assert Enroll.objects.filter(student=student).count() == 3

    unenroll_student(g12, student)
    assert Enroll.objects.filter(
        student=student, group__semester=s1
    ).count() == 1
    unenroll_student(g11, student)
    assert Enroll.objects.filter(
        student=student, group__semester=s1
    ).count() == 0
    unenroll_student(g2, student)
    assert Enroll.objects.filter(
        student=student, group__semester=s2
    ).count() == 0


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
