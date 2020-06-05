from datetime import date, datetime, timedelta
from typing import Tuple

import pytest
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from api.views.attendance import AttendanceErrors
from api.views.enroll import EnrollErrors
from sport.models import Enroll, Group, Trainer, Student, Training

before_training = datetime(2020, 1, 15, 17, 0, 0, tzinfo=timezone.utc)
training_start = datetime(2020, 1, 15, 18, 0, 0, tzinfo=timezone.utc)
training_end = datetime(2020, 1, 15, 20, 0, 0, tzinfo=timezone.utc)


@pytest.fixture
@pytest.mark.freeze_time(before_training)
def setup(
        semester_factory,
        sport_factory,
        group_factory,
        trainer_factory,
        student_factory,
        enroll_factory,
) -> Tuple[Training, Trainer, User]:
    semester_start = date(2020, 1, 1)
    semester_end = date(2020, 2, 20)
    choice_deadline = date(2020, 1, 10)
    sem = semester_factory(
        "S1",
        semester_start,
        semester_end,
        choice_deadline
    )

    trainer_user = trainer_factory(
        username="user",
        password="pass"
    )

    sport = sport_factory("sport1", False)
    group = group_factory(
        "G1",
        capacity=1,
        sport=sport,
        semester=sem,
        trainer=trainer_user.trainer,
        is_club=True,
    )

    training = Training.objects.create(
        group=group,
        schedule=None,
        start=training_start,
        end=training_end,
        training_class=None,
    )

    student_user = student_factory(
        username="student",
        password="student",
        email="student@example.com",
    )

    enroll_factory(student_user.student, group)

    return training, trainer_user, student_user


@pytest.mark.django_db
@pytest.mark.freeze_time(before_training)
def test_attendance_before_training(setup):
    training, trainer_user, student_user = setup
    client = APIClient()
    client.force_authenticate(trainer_user)

    data = {
        "training_id": training.pk,
        "student_hours": [
            {
                "student_id": student_user.student.pk,
                "hours": 1
            },
        ],
    }

    response = client.post(
        f"/{settings.PREFIX}api/attendance/mark",
        data=data
    )
    print(data)
    print(response.data)

    assert False
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    # assert response.data["code"] == AttendanceErrors.TRAINING_NOT_EDITABLE[0]
