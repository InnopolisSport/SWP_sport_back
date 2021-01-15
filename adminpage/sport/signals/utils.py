from datetime import datetime, time

from django.utils import timezone

from sport.models import Training, Attendance, Group


def update_attendance_record(
        group,
        upload_date,
        student,
        hours,
):

    tz = timezone.localtime().tzinfo
    training, _ = Training.objects.get_or_create(
        group=group,
        start=datetime.combine(upload_date, time(10, 0, 0), tzinfo=tz),
        end=datetime.combine(upload_date, time(20, 0, 0), tzinfo=tz)
    )
    attendance, _ = Attendance.objects.update_or_create(
        training=training,
        student=student,
        defaults={
            "hours": hours
        }
    )
