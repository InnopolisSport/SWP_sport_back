import pytest
import unittest
from datetime import date, time, datetime

from api.crud import get_attended_training_info, enroll_student_to_secondary_group, get_group_info, \
    get_trainings_for_student, get_trainings_for_trainer, get_trainings_in_time, get_students_grades
from sport.models import Training, Schedule

assertMembers = unittest.TestCase().assertCountEqual


@pytest.mark.django_db
@pytest.mark.freeze_time('2019-12-31 10:00')
def test_training_info(student_factory, trainer_factory, sport_factory, semester_factory, training_class_factory,
                          group_factory,
                          schedule_factory,
                          attendance_factory):
    student = student_factory("A1").student
    other_student = student_factory("A2").student
    trainer = trainer_factory("B").trainer
    sport = sport_factory(name="Sport")
    semester = semester_factory(name="S19", start=date(2020, 1, 1), end=date(2020, 1, 30),
                                choice_deadline=date(2020, 1, 15))
    training_class = training_class_factory(name="1337")
    group = group_factory(name="G1", sport=sport, semester=semester, capacity=20, trainer=trainer)
    schedule = schedule_factory(group=group, weekday=Schedule.Weekday.MONDAY, start=time(14, 0, 0), end=time(18, 30, 0),
                                training_class=training_class)

    trainings = Training.objects.all()
    t1 = trainings[0]
    t2 = trainings[1]
    t2.training_class = None
    t2.save()
    a1 = attendance_factory(training=t1, student=student, hours=1.5)
    assert get_attended_training_info(t1.pk, student) == {
        "group_id": group.pk,
        "group_name": group.name,
        "group_description": group.description,
        "training_class": training_class.name,
        "capacity": group.capacity,
        "current_load": 0,
        "trainer_first_name": trainer.user.first_name,
        "trainer_last_name": trainer.user.last_name,
        "trainer_email": trainer.user.email,
        "hours": a1.hours,
        "is_enrolled": False,
        "is_primary": False
    }
    assert get_group_info(group.pk, student) == {
        "group_id": group.pk,
        "group_name": group.name,
        "group_description": group.description,
        "capacity": group.capacity,
        "current_load": 0,
        "trainer_first_name": trainer.user.first_name,
        "trainer_last_name": trainer.user.last_name,
        "trainer_email": trainer.user.email,
        "is_enrolled": False,
        "is_primary": False
    }
    assertMembers(get_trainings_for_trainer(trainer=trainer, start=datetime(2020, 1, 1), end=datetime(2020, 1, 14)), [
        {
            "id": t1.pk,
            "start": t1.start,
            "end": t1.end,
            "group_id": group.pk,
            "group_name": group.name,
            "training_class": training_class.name,
            "can_grade": True
        },
        {
            "id": t2.pk,
            "start": t2.start,
            "end": t2.end,
            "group_id": group.pk,
            "group_name": group.name,
            "training_class": None,
            "can_grade": True
        }
    ])

    enroll_student_to_secondary_group(group, student)
    group.trainer = None
    group.save()
    assert get_attended_training_info(t2.pk, student) == {
        "group_id": group.pk,
        "group_name": group.name,
        "group_description": group.description,
        "training_class": None,
        "capacity": group.capacity,
        "current_load": 1,
        "trainer_first_name": None,
        "trainer_last_name": None,
        "trainer_email": None,
        "hours": None,
        "is_enrolled": True,
        "is_primary": False
    }
    assert get_group_info(group.pk, student) == {
        "group_id": group.pk,
        "group_name": group.name,
        "group_description": group.description,
        "capacity": group.capacity,
        "current_load": 1,
        "trainer_first_name": None,
        "trainer_last_name": None,
        "trainer_email": None,
        "is_enrolled": True,
        "is_primary": False
    }
    assertMembers(get_trainings_for_student(student=student, start=datetime(2020, 1, 1), end=datetime(2020, 1, 14)), [
        {
            "id": t1.pk,
            "start": t1.start,
            "end": t1.end,
            "group_id": group.pk,
            "group_name": group.name,
            "training_class": training_class.name,
            "hours": a1.hours,
            "can_grade": False
        },
        {
            "id": t2.pk,
            "start": t2.start,
            "end": t2.end,
            "group_id": group.pk,
            "group_name": group.name,
            "training_class": None,
            "hours": None,
            "can_grade": False
        }
    ])

    assert get_trainings_for_trainer(trainer=trainer, start=datetime(2020, 1, 1), end=datetime(2020, 1, 14)) == []

    assert get_trainings_in_time(sport_id=0, start=datetime(2020, 1, 1), end=datetime(2020, 1, 14)) == []
    assertMembers(get_trainings_in_time(sport_id=sport.pk, start=datetime(2020, 1, 1), end=datetime(2020, 1, 14)), [
        {
            "group_id": group.pk,
            "group_name": group.name,
            "current_load": 1,
            "capacity": group.capacity,
            "id": t2.pk,
            "start": t2.start,
            "end": t2.end,
            "training_class": None
        },
        {
            "group_id": group.pk,
            "group_name": group.name,
            "current_load": 1,
            "capacity": group.capacity,
            "id": t1.pk,
            "start": t1.start,
            "end": t1.end,
            "training_class": training_class.name,
        }
    ])

    assert get_students_grades(t1.pk) == [{
        "student_id": student.pk,
        "first_name": student.user.first_name,
        "last_name": student.user.last_name,
        "email": student.user.email,
        "hours": a1.hours
    }]
    assert get_students_grades(t2.pk) == [{
        "student_id": student.pk,
        "first_name": student.user.first_name,
        "last_name": student.user.last_name,
        "email": student.user.email,
        "hours": None
    }]

    enroll_student_to_secondary_group(group, other_student)

    assertMembers(get_students_grades(t1.pk), [
        {
            "student_id": student.pk,
            "first_name": student.user.first_name,
            "last_name": student.user.last_name,
            "email": student.user.email,
            "hours": a1.hours
        },
        {
            "student_id": other_student.pk,
            "first_name": other_student.user.first_name,
            "last_name": other_student.user.last_name,
            "email": other_student.user.email,
            "hours": None
        }
    ])
