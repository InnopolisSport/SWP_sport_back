import pytest

from sport.crud import enroll_student_to_secondary_group, enroll_student_to_primary_group, unenroll_student
from sport.models import Student, Semester, Group, Sport


@pytest.mark.django_db
def test_enroll(student_factory):
    student_factory("A")
    student = Student.objects.get()
    sport = Sport.objects.create(name="Sport")
    s1 = Semester.objects.create(name="S19")
    s2 = Semester.objects.create(name="S20")
    g11 = Group.objects.create(name="G11", sport=sport, semester=s1)
    g12 = Group.objects.create(name="G12", sport=sport, semester=s1)
    g2 = Group.objects.create(name="G2", sport=sport, semester=s2)

    assert Enroll.objects.filter(student=student).count() == 0
    enroll_student_to_primary_group(g11, student)
    assert Enroll.objects.filter(student=student).count() == 1
    enroll_student_to_primary_group(g12, student)
    assert Enroll.objects.filter(student=student).count() == 1
    enroll_student_to_primary_group(g2, student)
    assert Enroll.objects.filter(student=student).count() == 2

    unenroll_student(g2, student)
    assert Enroll.objects.filter(student=student).count() == 2

    Enroll.objects.all().delete()

    assert Enroll.objects.filter(student=student).count() == 0
    enroll_student_to_secondary_group(g11, student)
    assert Enroll.objects.filter(student=student).count() == 1
    enroll_student_to_secondary_group(g12, student)
    assert Enroll.objects.filter(student=student).count() == 2
    enroll_student_to_secondary_group(g2, student)
    assert Enroll.objects.filter(student=student).count() == 3

    unenroll_student(g2, student)
    assert Enroll.objects.filter(student=student).count() == 2
