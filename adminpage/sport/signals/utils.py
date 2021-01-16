from datetime import datetime, time

from django.utils import timezone

from sport.models import Training, Attendance, Group


def update_attendance_record(
        group,
        upload_date,
        student,
        hours,
        start=None,
        end=None,
        training_name=None,
):
    tz = timezone.localtime().tzinfo
    if start is None:
        start = datetime.combine(upload_date, time(7, 0, 0), tzinfo=tz)
    if end is None:
        end = datetime.combine(upload_date, time(9, 0, 0), tzinfo=tz)
    training, _ = Training.objects.get_or_create(
        group=group,
        start=start,
        end=end,
        custom_name=training_name,
    )
    attendance, _ = Attendance.objects.update_or_create(
        training=training,
        student=student,
        defaults={
            "hours": hours
        }
    )
