from datetime import datetime, time
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from django.conf import settings
from django.utils import timezone

from sport.models import Reference, Training, Attendance, Group
from sport.signals.utils import update_attendance_record


@receiver(post_save, sender=Reference)
def update_hours_for_reference(sender, instance: Reference, created, **kwargs):
    if created:
        return

    # get_or_create returns (object: Model, created: bool)
    group = Group.objects.get(
        semester=instance.semester,
        name=settings.MEDICAL_LEAVE_GROUP_NAME
    )

    update_attendance_record(
        group=group,
        upload_date=instance.uploaded.date(),
        student=instance.student,
        hours=instance.hours
    )
