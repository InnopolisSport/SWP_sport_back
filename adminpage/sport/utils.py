from datetime import date
from enum import IntEnum

from django.conf import settings
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils import timezone

class SubmissionType(IntEnum):
    LINK = 1
    IMAGE = 0


def format_submission_html(
        submission_type: SubmissionType,
        submission_url: str
) -> str:
    if submission_type == SubmissionType.LINK:
        return format_html('<a href="{}">link</a>', submission_url)
    elif submission_type == SubmissionType.IMAGE:
        return format_html(
            '<a href="{}{}">image</a>',
            mark_safe(settings.BASE_URL),
            submission_url,
        )
    else:
        raise ValueError(f"Got unknown submission type: {submission_type}")


def get_study_year_from_date(in_date: date) -> int:
    new_semester_start = date.today().replace(month=8, day=20)
    delta_year = -1 if in_date < new_semester_start else 0
    return in_date.year + delta_year


def get_current_study_year() -> int:
    return get_study_year_from_date(date.today())


def set_session_notification(request, msg: str, msg_type: str):
    request.session["notify"] = (msg_type, msg)

def today() -> date:
    return timezone.now().date()
