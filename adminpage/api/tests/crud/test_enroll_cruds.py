import pytest
from datetime import date

from api.crud import enroll_student, unenroll_student
from sport.models import Enroll

dummy_date = date(2020, 1, 1)


@pytest.mark.django_db
def test_enroll(student_factory, sport_factory, semester_factory, group_factory):
    student = student_factory("A@foo.bar").student
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
    assert Enroll.objects.filter(student=student).count() == 2
    unenroll_student(g11, student)
    assert Enroll.objects.filter(student=student).count() == 2
    unenroll_student(g2, student)
    assert Enroll.objects.filter(student=student).count() == 2
