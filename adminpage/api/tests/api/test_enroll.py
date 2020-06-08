from datetime import date, datetime
from typing import Tuple

import pytest
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from api.views.enroll import EnrollErrors
from sport.models import Enroll, Group

start = date(2020, 1, 1)
end = date(2020, 2, 20)
choice_deadline = date(2020, 1, 21)
just_before_deadline = datetime(2020, 1, 21, 23, 0, 0, tzinfo=timezone.get_default_timezone())
just_after_deadline = datetime(2020, 1, 22, 0, 1, 5, tzinfo=timezone.get_default_timezone())


@pytest.fixture
def setup_group(
        semester_factory,
        sport_factory,
        group_factory,
) -> Group:
    sem = semester_factory(
        "S1",
        start,
        end,
        choice_deadline
    )

    sport = sport_factory("sport1", False)
    group = group_factory(
        "G1",
        capacity=1,
        sport=sport,
        semester=sem,
        trainer=None,
        is_club=True,
    )
    return group


@pytest.fixture
def logged_in_student(student_factory) -> Tuple[APIClient, User]:
    username = "user"
    password = "pass"
    student_user = student_factory(
        username=username,
        password=password,
    )
    client = APIClient()
    client.login(
        username=username,
        password=password,
    )
    return client, student_user


@pytest.mark.django_db
@pytest.mark.freeze_time(just_before_deadline)
def test_enroll_primary_success(setup_group: Group, logged_in_student):
    client, student_user = logged_in_student

    response = client.post(
        f"/{settings.PREFIX}api/enrollment/enroll",
        data={
            "group_id": setup_group.pk,
        }
    )
    assert response.status_code == status.HTTP_200_OK
    assert Enroll.objects.filter(
        student=student_user.student,
        group=setup_group,
        is_primary=True
    ).count() == 1


@pytest.mark.django_db
@pytest.mark.freeze_time(just_before_deadline)
def test_enroll_primary_update(setup_group: Group, logged_in_student, group_factory):
    client, student_user = logged_in_student
    g2 = group_factory(
        "G2",
        capacity=1,
        sport=setup_group.sport,
        semester=setup_group.semester,
        trainer=setup_group.trainer,
        is_club=setup_group.is_club,
    )

    response = client.post(
        f"/{settings.PREFIX}api/enrollment/enroll",
        data={
            "group_id": setup_group.pk,
        }
    )
    assert response.status_code == status.HTTP_200_OK
    assert Enroll.objects.filter(
        student=student_user.student,
        group=setup_group,
        is_primary=True
    ).count() == 1

    response = client.post(
        f"/{settings.PREFIX}api/enrollment/enroll",
        data={
            "group_id": g2.pk,
        }
    )

    assert response.status_code == status.HTTP_200_OK
    assert Enroll.objects.filter(
        student=student_user.student,
        is_primary=True
    ).count() == 1
    assert Enroll.objects.filter(
        student=student_user.student,
        group=g2,
        is_primary=True
    ).count() == 1


@pytest.mark.django_db
@pytest.mark.freeze_time(just_before_deadline)
def test_enroll_primary_full_group(setup_group: Group, logged_in_student):
    client, student_user = logged_in_student
    setup_group.capacity = 0
    setup_group.save()
    response = client.post(
        f"/{settings.PREFIX}api/enrollment/enroll",
        data={
            "group_id": setup_group.pk,
        }
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["code"] == EnrollErrors.GROUP_IS_FULL[0]
    assert Enroll.objects.filter(
        student=student_user.student,
    ).count() == 0


@pytest.mark.django_db
@pytest.mark.freeze_time(just_after_deadline)
def test_enroll_secondary_success(setup_group: Group, logged_in_student):
    client, student_user = logged_in_student

    response = client.post(
        f"/{settings.PREFIX}api/enrollment/enroll",
        data={
            "group_id": setup_group.pk,
        }
    )
    assert response.status_code == status.HTTP_200_OK
    assert Enroll.objects.filter(
        student=student_user.student,
        group=setup_group,
        is_primary=False
    ).count() == 1


@pytest.mark.django_db
@pytest.mark.freeze_time(just_after_deadline)
def test_enroll_secondary_full_group(setup_group: Group, logged_in_student):
    client, student_user = logged_in_student
    setup_group.capacity = 0
    setup_group.save()
    response = client.post(
        f"/{settings.PREFIX}api/enrollment/enroll",
        data={
            "group_id": setup_group.pk,
        }
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["code"] == EnrollErrors.GROUP_IS_FULL[0]
    assert Enroll.objects.filter(
        student=student_user.student,
    ).count() == 0


@pytest.mark.django_db
@pytest.mark.freeze_time
def test_enroll_double_enroll(setup_group: Group, logged_in_student, freezer):
    freezer.move_to(just_before_deadline)
    client, student_user = logged_in_student

    response = client.post(
        f"/{settings.PREFIX}api/enrollment/enroll",
        data={
            "group_id": setup_group.pk,
        }
    )
    assert response.status_code == status.HTTP_200_OK
    assert Enroll.objects.filter(
        student=student_user.student,
        group=setup_group,
        is_primary=True
    ).count() == 1

    freezer.move_to(just_after_deadline)

    response = client.post(
        f"/{settings.PREFIX}api/enrollment/enroll",
        data={
            "group_id": setup_group.pk,
        }
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["code"] == EnrollErrors.DOUBLE_ENROLL[0]


@pytest.mark.django_db
@pytest.mark.freeze_time(just_after_deadline)
def test_enroll_secondary_too_many_secondary_groups(
        setup_group: Group,
        logged_in_student,
        group_factory
):
    client, student_user = logged_in_student
    groups = [setup_group]
    # setup group is G1, others are G2 and G3
    # 1 primary and 2 secondary are permitted,
    # so generate 2 groups
    for i in range(2, 4):
        g = group_factory(
            "G" + str(i),
            capacity=1,
            sport=setup_group.sport,
            semester=setup_group.semester,
            trainer=setup_group.trainer,
            is_club=setup_group.is_club,
        )
        groups.append(g)

    for group in groups[:-1]:
        response = client.post(
            f"/{settings.PREFIX}api/enrollment/enroll",
            data={
                "group_id": group.pk,
            }
        )
        assert response.status_code == status.HTTP_200_OK

    response = client.post(
        f"/{settings.PREFIX}api/enrollment/enroll",
        data={
            "group_id": groups[-1].pk,
        }
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["code"] == EnrollErrors.TOO_MUCH_SECONDARY[0]
    assert Enroll.objects.filter(
        student=student_user.student,
    ).count() == 2


@pytest.mark.django_db
@pytest.mark.freeze_time(just_after_deadline)
def test_unenroll_secondary(setup_group: Group, logged_in_student, enroll_factory):
    client, student_user = logged_in_student
    enroll_factory(
        student_user.student,
        setup_group,
        is_primary=False
    )

    response = client.post(
        f"/{settings.PREFIX}api/enrollment/unenroll",
        data={
            "group_id": setup_group.pk,
        }
    )

    assert response.status_code == status.HTTP_200_OK
    assert Enroll.objects.count() == 0


@pytest.mark.django_db
@pytest.mark.freeze_time(just_after_deadline)
def test_unenroll_primary(setup_group: Group, logged_in_student, enroll_factory):
    client, student_user = logged_in_student
    enrollment = enroll_factory(
        student_user.student,
        setup_group,
        is_primary=True
    )

    response = client.post(
        f"/{settings.PREFIX}api/enrollment/unenroll",
        data={
            "group_id": setup_group.pk,
        }
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["code"] == EnrollErrors.PRIMARY_UNENROLL[0]
    assert Enroll.objects.count() == 1
