from datetime import datetime, time
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from django.conf import settings
from django.utils import timezone

from sport.models import Reference, Training, Attendance, Group


@receiver(post_save, sender=Reference)
def update_hours_for_reference(sender, instance: Reference, created, **kwargs):
    if created and instance.hours == 0:
        return

    # get_or_create returns (object: Model, created: bool)
    group = Group.objects.get(semester=instance.semester, name=settings.MEDICAL_LEAVE_GROUP_NAME)
    upload_date = instance.uploaded.date()
    tz = timezone.localtime().tzinfo
    medical_training, _ = Training.objects.get_or_create(group=group,
                                                         start=datetime.combine(upload_date, time(10, 0, 0), tzinfo=tz),
                                                         end=datetime.combine(upload_date, time(20, 0, 0), tzinfo=tz)
                                                         )

    if instance.hours == 0:
        Attendance.objects.filter(training=medical_training, student=instance.student).delete()
    else:
        attendance, _ = Attendance.objects.get_or_create(training=medical_training, student=instance.student)
        attendance.hours = instance.hours
        attendance.save()
