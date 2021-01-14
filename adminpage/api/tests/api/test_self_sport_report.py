import tempfile
from datetime import date

import pytest
from PIL import Image
from django.conf import settings
from rest_framework import status
from rest_framework.test import APIClient

from sport.models import SelfSportReport


@pytest.mark.django_db
@pytest.mark.freeze_time(date(2020, 1, 2))
def test_reference_upload_image(
        student_factory,
        semester_factory,
        freezer
):
    email = "user@foo.bar"
    password = "pass"
    student = student_factory(
        email=email,
        password=password,
    )
    semester = semester_factory(
        name="S20",
        start=date(2020, 1, 1),
        end=date(2020, 1, 15),
    )
    client = APIClient()
    client.login(
        email=email,
        password=password,
    )

    image_md = Image.new('RGB', (600, 600))
    file_md = tempfile.NamedTemporaryFile(suffix='.jpg')
    image_md.save(file_md)
    file_md.seek(0)

    response = client.post(
        f"/{settings.PREFIX}api/selfsport/upload",
        data={"image": file_md, },
        format='multipart'
    )

    assert response.status_code == status.HTTP_200_OK
    assert SelfSportReport.objects.filter(
        semester=semester,
        student__pk=student.pk,
    ).count() == 1
    report = SelfSportReport.objects.filter(
        semester=semester,
        student__pk=student.pk,
    ).first()

    assert report.link is None
    assert report.image is not None


@pytest.mark.django_db
@pytest.mark.freeze_time(date(2020, 1, 2))
def test_reference_upload_image_link(
        student_factory,
        semester_factory,
        freezer
):
    email = "user@foo.bar"
    password = "pass"
    student = student_factory(
        email=email,
        password=password,
    )
    semester = semester_factory(
        name="S20",
        start=date(2020, 1, 1),
        end=date(2020, 1, 15),
    )
    client = APIClient()
    client.login(
        email=email,
        password=password,
    )

    image_md = Image.new('RGB', (600, 600))
    file_md = tempfile.NamedTemporaryFile(suffix='.jpg')
    image_md.save(file_md)
    file_md.seek(0)

    response = client.post(
        f"/{settings.PREFIX}api/selfsport/upload",
        data={
            "image": file_md,
            "link": "https://google.com",
        },
        format='multipart'
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
@pytest.mark.freeze_time(date(2020, 1, 2))
def test_reference_upload_image_invalid_size(
        student_factory,
        semester_factory,
        freezer
):
    email = "user@foo.bar"
    password = "pass"
    student = student_factory(
        email=email,
        password=password,
    )
    semester = semester_factory(
        name="S20",
        start=date(2020, 1, 1),
        end=date(2020, 1, 15),
    )
    client = APIClient()
    client.login(
        email=email,
        password=password,
    )

    image_sm = Image.new('RGB', (600, 300))
    image_lg = Image.new('RGB', (600, 5500))
    file_sm = tempfile.NamedTemporaryFile(suffix='.jpg')
    file_lg = tempfile.NamedTemporaryFile(suffix='.jpg')
    image_sm.save(file_sm)
    image_lg.save(file_lg)
    file_sm.seek(0)
    file_lg.seek(0)

    response = client.post(
        f"/{settings.PREFIX}api/selfsport/upload",
        data={"image": file_sm, },
        format='multipart'
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    response = client.post(
        f"/{settings.PREFIX}api/selfsport/upload",
        data={"image": file_lg, },
        format='multipart'
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
