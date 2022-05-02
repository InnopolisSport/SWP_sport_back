import unittest
from datetime import date

import pytest
import requests
from django.conf import settings
from django.db.models import Sum
from rest_framework import status
from rest_framework.test import APIClient

from api.views.utils import parse_activity_app_name, evaluate_activity, parse_training_peaks_activity_info
from sport.models import SelfSportReport, SelfSportType, Attendance, Group

frozen_time = date(2020, 1, 2)
semester_start = date(2020, 1, 1)
semester_end = date(2020, 1, 15)
assertMembers = unittest.TestCase().assertEqual


@pytest.fixture
@pytest.mark.freeze_time(frozen_time)
def setup(
    student_factory,
    semester_factory,
):
    email = "user@foo.bar"
    password = "pass"
    student = student_factory(
        email=email,
        password=password,
    )

    student.student.medical_group_id = \
        settings.SELFSPORT_MINIMUM_MEDICAL_GROUP_ID
    student.save()

    semester = semester_factory(
        name="S20",
        start=semester_start,
        end=semester_end,
    )
    selfsport_type, _ = SelfSportType.objects.get_or_create(
        name="self_sport",
        defaults={
            "application_rule": "just apply",
            "is_active": True,
        }
    )
    client = APIClient()
    client.login(
        email=email,
        password=password,
    )
    return student, semester, selfsport_type, client


@pytest.mark.django_db
@pytest.mark.freeze_time(frozen_time)
def test_reference_upload_link_only(
    setup,
    freezer
):
    student, semester, selfsport_type, client = setup

    response = client.post(
        f"/{settings.PREFIX}api/selfsport/upload",
        data={
            "link": "https://strava.com/activities/1",
            "training_type": selfsport_type.pk,
        },
        format='multipart'
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
@pytest.mark.freeze_time(frozen_time)
def test_reference_upload_invalid_link(
    setup,
    freezer
):
    student, semester, selfsport_type, client = setup

    response = client.post(
        f"/{settings.PREFIX}api/selfsport/upload",
        data={
            "link": "https://google.com",
            "hours": 2,
            "training_type": selfsport_type.pk,
        },
        format='multipart'
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
@pytest.mark.freeze_time(frozen_time)
def test_reference_upload_valid_link(
    setup,
    freezer
):
    student, semester, selfsport_type, client = setup

    response = client.post(
        f"/{settings.PREFIX}api/selfsport/upload",
        data={
            "link": "https://www.strava.com/activities/5324378543",
            "hours": 2,
            "training_type": selfsport_type.pk,
        },
        format='multipart'
    )

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
@pytest.mark.freeze_time(frozen_time)
def test_reference_upload_more_three_hours(
    setup,
    freezer
):
    student, semester, selfsport_type, client = setup

    response = client.post(
        f"/{settings.PREFIX}api/selfsport/upload",
        data={
            "link": "https://www.strava.com/activities/5324378543",
            "hours": 2,
            "training_type": selfsport_type.pk,
        },
        format='multipart'
    )

    assert response.status_code == status.HTTP_200_OK


# @pytest.mark.django_db
# @pytest.mark.freeze_time(frozen_time)
# def test_self_sport_same_type_same_day(
#         setup,
#         freezer
# ):
#     student, semester, selfsport_type, client = setup
#     self_sport_group = Group.objects.get(
#         semester=semester,
#         name=settings.SELF_TRAINING_GROUP_NAME
#     )
#     report1 = SelfSportReport.objects.create(
#         student_id=student.pk,
#         semester=semester,
#         link="https://www.strava.com/activities/5324378542",
#         training_type=selfsport_type
#     )
#     report1.save()
#     report2 = SelfSportReport.objects.create(
#         student_id=student.pk,
#         semester=semester,
#         link="https://www.strava.com/activities/5324378543",
#         training_type=selfsport_type
#     )
#     report2.save()
#
#     report1.hours = 5
#     report1.save()
#
#     report2.hours = 7
#     report2.save()
#     assert Attendance.objects.filter(
#         student_id=student.pk,
#         training__group=self_sport_group,
#     ).aggregate(Sum("hours"))["hours__sum"] == report1.hours + report2.hours


# @pytest.mark.django_db
# @pytest.mark.freeze_time(frozen_time)
# def test_valid_strava_link_parsing(
#         setup,
#         freezer
# ):
#     student, semester, selfsport_type, client = setup
#
#     response = client.get(
#         f"/{settings.PREFIX}api/selfsport/activity_parsing",
#         data={
#             "link": "https://www.strava.com/activities/5324378542"
#         },
#         format='multipart'
#     )
#
#     if response.status_code != status.HTTP_429_TOO_MANY_REQUESTS:
#         assert response.status_code == status.HTTP_200_OK
#         assertMembers(response.data, {
#             'distance_km': 2.5,
#             'type': 'RUNNING',
#             'speed': 10.0,
#             'hours': 1,
#             'approved': True
#             }
#         )


# @pytest.mark.django_db
# @pytest.mark.freeze_time(frozen_time)
# def test_invalid_strava_link_parsing(
#         setup,
#         freezer
# ):
#     student, semester, selfsport_type, client = setup
#
#     response = client.get(
#         f"/{settings.PREFIX}api/selfsport/activity_parsing",
#         data={
#             "link": "https://www.strava.com/activities/5"
#         },
#         format='multipart'
#     )
#
#     assert response.status_code == status.HTTP_400_BAD_REQUEST


# @pytest.mark.django_db
# @pytest.mark.freeze_time(frozen_time)
# def test_invalid_link_parsing(
#         setup,
#         freezer
# ):
#     student, semester, selfsport_type, client = setup
#
#     response = client.get(
#         f"/{settings.PREFIX}api/selfsport/activity_parsing",
#         data={
#             "link": "https://www.google.com"
#         },
#         format='multipart'
#     )
#
#     assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
@pytest.mark.freeze_time(frozen_time)
def test_reference_upload_duplicate_link(
    setup,
    freezer
):
    student, semester, selfsport_type, client = setup

    response = client.post(
        f"/{settings.PREFIX}api/selfsport/upload",
        data={
            "link": "https://www.strava.com/activities/5324378543",
            "hours": 2,
            "training_type": selfsport_type.pk,
        },
        format='multipart'
    )

    assert response.status_code == status.HTTP_200_OK

    response = client.post(
        f"/{settings.PREFIX}api/selfsport/upload",
        data={
            "link": "https://www.strava.com/activities/5324378543",
            "hours": 2,
            "training_type": selfsport_type.pk,
        },
        format='multipart'
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_parse_activity_app_name():
    assert parse_activity_app_name('https://strava.com/activities/6117701711') == 'strava'
    assert parse_activity_app_name('https://strava.app.link/Fod1LyoHCkb') == 'strava'
    assert parse_activity_app_name('https://home.trainingpeaks.com/athlete/workout/PGCXDWA4MZLVZTI4FEYTRMETSU') \
           == 'training_peaks'
    assert parse_activity_app_name('http://tpks.ws/PGCXDWA4MZLVZTI4FEYTRMETSU') == 'training_peaks'
    assert parse_activity_app_name('http://google.com') is None


def test_parse_training_peaks_activity_info():
    # Running
    link = 'http://tpks.ws/PGCXDWA4MZLVZTI4FEYTRMETSU'
    html = requests.get(link).text
    expected_result = {'training_type': 'Running',
                       'distance': 6.02,
                       'avg_heart_rate': 132,
                       'avg_speed': 10.44,
                       'hours': 1,
                       'approved': True}
    assert parse_training_peaks_activity_info(html) == expected_result

    # Walking
    link = 'http://tpks.ws/DOOZKVTMPNUDFTI4FEYTRMETSU'
    html = requests.get(link).text
    expected_result = {'training_type': 'Walking',
                       'distance': 6.26,
                       'avg_heart_rate': 98,
                       'avg_speed': 4.24,
                       'hours': 1,
                       'approved': False}
    assert parse_training_peaks_activity_info(html) == expected_result

    # Biking
    link = 'http://tpks.ws/NSZ3SBNB6LFUTTI4FEYTRMETSU'
    html = requests.get(link).text
    expected_result = {'training_type': 'Biking',
                       'distance': 39.44,
                       'avg_heart_rate': 142,
                       'avg_speed': 29.99,
                       'hours': 2,
                       'approved': True}
    assert parse_training_peaks_activity_info(html) == expected_result

    # Swimming
    link = 'http://tpks.ws/CYU4LCMPDI6E7TI4FEYTRMETSU'
    html = requests.get(link).text
    expected_result = {'training_type': 'Swimming',
                       'distance': 5.17,
                       'avg_heart_rate': 141,
                       'avg_speed': 3.97,
                       'hours': 3,
                       'approved': True}
    assert parse_training_peaks_activity_info(html) == expected_result
