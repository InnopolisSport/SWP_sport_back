import pytest
from datetime import date
from django.utils import timezone

from sport.crud import get_detailed_hours, get_brief_hours, mark_hours, toggle_illness
from sport.models import Student, Attendance

dummy_date = date(2020, 1, 1)

@pytest.mark.django_db
def test_hours_statistics(student_factory, sport_factory, semester_factory, group_factory, training_factory, attendance_factory):
    student_factory("A")
    student_factory("B")
    student, other_student = list(Student.objects.all())
    sport = sport_factory(name="Sport")
    s1 = semester_factory(name="S19", start=dummy_date, end=dummy_date, choice_deadline=dummy_date)
    s2 = semester_factory(name="S20", start=dummy_date, end=dummy_date, choice_deadline=dummy_date)
    g11 = group_factory(name="G11", sport=sport, semester=s1, capacity=20)
    g12 = group_factory(name="G12", sport=sport, semester=s1, capacity=20)
    g21 = group_factory(name="G21", sport=sport, semester=s2, capacity=20)
    g22 = group_factory(name="G22", sport=sport, semester=s2, capacity=20)

    trainings = []
    for i, g in enumerate([g11, g12, g21, g22]):
        t = training_factory(group=g, start=timezone.now(), end=timezone.now())
        trainings.append(t)
        attendance_factory(training=t, student=student, hours=i + 1)
        attendance_factory(training=t, student=other_student, hours=1)
    brief = get_brief_hours(student)
    assert brief == [
        {
            "hours": 3,
            "semester_id": s1.pk,
            "semester_name": s1.name,
            "semester_start": s1.start,
            "semester_end": s1.end
        },
        {
            "hours": 7,
            "semester_id": s2.pk,
            "semester_name": s2.name,
            "semester_start": s2.start,
            "semester_end": s2.end
        }
    ]
    stat1 = get_detailed_hours(student, s1)
    stat2 = get_detailed_hours(student, s2)
    assert stat1 == [
        {
            "group": g12.name,
            "timestamp": trainings[1].start,
            "hours": 2
        },
        {
            "group": g11.name,
            "timestamp": trainings[0].start,
            "hours": 1
        }
    ]
    assert stat2 == [
        {
            "group": g22.name,
            "timestamp": trainings[3].start,
            "hours": 4
        },
        {
            "group": g21.name,
            "timestamp": trainings[2].start,
            "hours": 3
        }
    ]


@pytest.mark.django_db
def test_mark_hours(student_factory, sport_factory, semester_factory, group_factory, training_factory):
    student_factory("A")
    student_factory("B")
    student1, student2 = list(Student.objects.all())
    sport = sport_factory(name="Sport")
    semester = semester_factory(name="S19", start=dummy_date, end=dummy_date, choice_deadline=dummy_date)
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
    student_factory("A")
    student = Student.objects.get()
    assert not student.is_ill
    toggle_illness(student)
    assert student.is_ill
    toggle_illness(student)
    assert not student.is_ill
