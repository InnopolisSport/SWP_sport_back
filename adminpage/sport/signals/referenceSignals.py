from datetime import datetime, time
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from django.conf import settings
from django.utils import timezone

from sport.models import Reference, Training, Attendance, Group, MedicalGroupReference


@receiver(post_save, sender=Reference)
def update_hours_for_reference(sender, instance: Reference, created, **kwargs):
    if created:
        return

    # get_or_create returns (object: Model, created: bool)
    group = Group.objects.get(semester=instance.semester, name=settings.MEDICAL_LEAVE_GROUP_NAME)
    upload_date = instance.uploaded.date()
    tz = timezone.localtime().tzinfo
    medical_training, _ = Training.objects.get_or_create(group=group,
                                                         start=datetime.combine(upload_date, time(0, 0, 0), tzinfo=tz),
                                                         end=datetime.combine(upload_date, time(23, 59, 59), tzinfo=tz)
                                                         )

    attendance, _ = Attendance.objects.update_or_create(training=medical_training, student=instance.student, defaults={
        "hours": instance.hours
    })

    if instance.hours > 0:
        instance.student.notify(
            '[IU Sport] Reference Accepted',
            f'Your reference from {instance.uploaded.date()} got accepted. You got {instance.hours} hours for it.',
        )
    else:
        instance.student.notify(
            '[IU Sport] Reference Rejected',
            f'Your reference from {instance.uploaded.date()} got rejected.\nComment:\n{instance.comment}',
        )


@receiver(post_save, sender=MedicalGroupReference)
def medical_group_updated(sender, instance: MedicalGroupReference, created, **kwargs):
    if created or instance.resolved is None:
        return

    if instance.resolved:
        instance.student.notify(
            '[IU Sport] Medical Group Reference Processed',
            f'Your medical group reference for semester {instance.semester} was processed.\n'
            f'You were assigned a medical group "{instance.student.medical_group.name}".' +
            ('' if len(instance.comment) == 0 else f'\nComment: {instance.comment}'),
        )
    else:
        instance.student.notify(
            '[IU Sport] Medical Group Reference Rejected',
            f'Your medical group reference for semester {instance.semester} was rejected.\n'
            f'Please, submit a new reference or contact the course support.\n'
            f'Comment: {instance.comment}'
        )
