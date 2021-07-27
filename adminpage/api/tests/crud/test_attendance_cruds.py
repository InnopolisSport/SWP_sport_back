import pytest
import unittest
from datetime import date
from django.utils import timezone

from api.crud import get_detailed_hours, get_brief_hours, mark_hours, toggle_illness
from sport.models import Attendance

dummy_date = date(2020, 1, 1)

assertMembers = unittest.TestCase().assertCountEqual


@pytest.mark.django_db
def test_mark_hours(student_factory, sport_factory, semester_factory, group_factory, training_factory):
    student1 = student_factory("A@foo.bar").student
    student2 = student_factory("B@foo.bar").student
    sport = sport_factory(name="Sport")
    semester = semester_factory(name="S19", start=dummy_date, end=dummy_date)
    group = group_factory(name="G1", sport=sport, semester=semester, capacity=20)
    training = training_factory(group=group, start=timezone.now(), end=timezone.now())
    mark_hours(training, [
        (student1.pk, 1.5),
        (student2.pk, 2.5)
    ])
    attendance1 = Attendance.objects.get(student=student1)
    attendance2 = Attendance.objects.get(student=student2)
    assert attendance1.hours == 1.5
    assert attendance2.hours == 2.5
    mark_hours(training, [
        (student1.pk, 3.5),
        (student2.pk, 0)
    ])
    attendance1 = Attendance.objects.get(student=student1)
    assert attendance1.hours == 3.5
    assert Attendance.objects.count() == 1


@pytest.mark.django_db
def test_toggle_illness(student_factory):
    student = student_factory("A@foo.bar").student
    assert not student.is_ill
    toggle_illness(student)
    assert student.is_ill
    toggle_illness(student)
    assert not student.is_ill
